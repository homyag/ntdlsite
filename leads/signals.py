import os
import json
import requests

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.forms import model_to_dict

from .models import Call

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

# operator_id = 809618451 #Ксюша
operator_id = 59726568 #admin


def send_telegram_message(user_id, message, reply_markup=None):
    bot_token = BOT_TOKEN
    url = f'https://api.telegram.org/bot{bot_token}/sendMessage'
    data = {
        'chat_id': user_id,
        'text': message,
        'parse_mode': 'HTML'  # Опционально, если использовать HTML в сообщении
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)

    response = requests.post(url, data=data)
    return response.json()

#функция генерации клавиатуры для уведомлений из django-signals
def action_choice_keyboard(task_id):
    keyboard = {
        "inline_keyboard": [
            [
                {"text": "Добавить комментарий", "callback_data": f"edit_comment:{task_id}"}
            ],
            [
                {"text": "Изменить статус", "callback_data": f"edit_status:{task_id}"}
            ],
            [
                {"text": "Передать другому менеджеру", "callback_data": f"edit_manager:{task_id}"}
            ],
        ]
    }
    return keyboard

original_manager = None

@receiver(pre_save, sender=Call)
def set_original_manager(sender, instance, **kwargs):
    global original_manager
    if instance.pk:  # Если запись уже существует
        original_manager = Call.objects.get(pk=instance.pk).manager
    else:
        original_manager = None

@receiver(post_save, sender=Call)
def notify_manager_on_call_creation(sender, instance, created, **kwargs):
    if created and instance.manager.tg_id:
        manager = instance.manager
        message = (
            f'Уважаемый(ая), {manager.name},\n\n'
            f'Вам была назначена заявка № {instance.id}:\n'
            f'Клиент: {instance.name}\n'
            f'Телефон: {instance.phone}\n'
            f'Email: {instance.mail}\n\n'
            f'Комментарий: {instance.comment}\n\n'
            f'Пожалуйста, свяжитесь с клиентом.\n\n'
            f'Срок исполнения до: {instance.date_of_notification}'
        )
        keyboard = action_choice_keyboard(instance.id)
        send_telegram_message(manager.tg_id, message, reply_markup=keyboard)
        send_telegram_message(operator_id, message, reply_markup=keyboard)

# оповещение при изменении записи в админке
@receiver(post_save, sender=Call)
def notify_users_on_call_change(sender, instance, created, **kwargs):
    global original_manager
    if not created:
        if instance.manager != original_manager:
            # отправка уведомления новому менеджеру
            new_manager = instance.manager
            if new_manager.tg_id:
                message = (
                    f'Уважаемый(ая), <b>{new_manager.name}</b>,\n\n'
                    f'Вам была передана заявка № <b>{instance.id}</b> от <b>{original_manager.name}</b>:\n'
                    f'Клиент: <b>{instance.name}</b>\n'
                    f'Телефон: <b>{instance.phone}</b>\n'
                    f'Email: <b>{instance.mail}</b>\n\n'
                    f'Комментарий: <b>{instance.comment}</b>\n\n'
                    f'Пожалуйста, свяжитесь с клиентом.\n\n'
                    f'Срок исполнения до: <b>{instance.date_of_notification}</b>'
                )
                keyboard = action_choice_keyboard(instance.id)
                send_telegram_message(new_manager.tg_id, message,
                                      reply_markup=keyboard)
                # Отправка уведомления оператору
                message_to_operator = (
                    f'Заявка № <b>{instance.id}</b> была передана новому '
                    f'менеджеру <b>{new_manager.name}</b> от <b>{original_manager.name}</b>:\n'
                    f'Клиент: <b>{instance.name}</b>\n'
                    f'Телефон: <b>{instance.phone}</b>\n'
                    f'Email: <b>{instance.mail}</b>\n\n'
                    f'Комментарий: <b>{instance.comment}</b>\n\n'
                    f'Срок исполнения до: <b>{instance.date_of_notification}</b>'
                )
                send_telegram_message(operator_id, message_to_operator)

            # отправка уведомления о любом изменении заявки
        else:
            message = (
                f'Заявка № <b>{instance.id}</b> от <b>{instance.created}</b>, '
                f'ответственный менеджер <b>{instance.manager}</b>, была '
                f'обновлена:\n'
                f'Клиент: <b>{instance.name}</b>\n'
                f'Телефон: <b>{instance.phone}</b>\n'
                f'Email: <b>{instance.mail}</b>\n\n'
                f'Комментарий: <b>{instance.comment}</b>\n\n'
                f'Срок исполнения до: <b>{instance.date_of_notification}</b>'
            )
            send_telegram_message(operator_id, message)
