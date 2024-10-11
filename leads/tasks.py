from celery import shared_task
from datetime import date

from .models import Call
from .signals import send_telegram_message
from new_tdl_site.celery import app


@shared_task
def check_notifications():
    today = date.today()
    calls = Call.objects.filter(date_of_notification=today)
    lost_calls = Call.objects.filter(date_of_notification__lt=today)

    # Группируем заявки по менеджеру
    calls_by_manager = {}
    for call in calls:
        manager = call.manager
        if manager not in calls_by_manager:
            calls_by_manager[manager] = []
        calls_by_manager[manager].append(call)

    # Отправляем уведомления для сегодняшних заявок
    for manager, manager_calls in calls_by_manager.items():
        user_id = manager.tg_id
        message = (
            f"Уважаемый(ая), {manager.name}\n\n"
            f"Сегодня {today} подходит срок исполнения заявок:\n"
        )
        for call in manager_calls:
            message += (
                f'Заявка № {call.id} от {call.created}\n'
                f'Клиент: {call.name}\n'
                f'Телефон: {call.phone}\n'
                f'Комментарий: {call.comment}\n\n'
            )
        if user_id and message:
            send_telegram_message(user_id, message)

    # Группируем просроченные заявки по менеджеру
    lost_calls_by_manager = {}
    for lost_call in lost_calls:
        manager = lost_call.manager
        if manager not in lost_calls_by_manager:
            lost_calls_by_manager[manager] = []
        lost_calls_by_manager[manager].append(lost_call)

    # Отправляем уведомления для просроченных заявок
    for manager, manager_lost_calls in lost_calls_by_manager.items():
        user_id = manager.tg_id
        message = (
            f"На сегодня {today} у Вас не закрыты следующие заявки:\n"
        )
        for lost_call in manager_lost_calls:
            message += (
                f'Заявка № {lost_call.id} от {lost_call.created}\n'
                f'Клиент: {lost_call.name}\n'
                f'Телефон: {lost_call.phone}\n'
                f'Комментарий: {lost_call.comment}\n\n'
            )
        message += (
            f'Пожалуйста, свяжитесь с клиентом.\n\n'
            f'Для изменения статуса заявки воспользуйтесь командой /mytasks '
            f'или обратитесь к оператору.'
        )
        if user_id and message:
            send_telegram_message(user_id, message)