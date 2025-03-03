from .models import CallbackRequest, FeedbackRequest

from django.db.models.signals import post_save
from django.dispatch import receiver

from leads.signals import send_telegram_message
from leads.signals import admin_id
from leads.signals import operator_id


@receiver(post_save, sender=CallbackRequest)
def notify_operator_on_callback_request(sender, instance, created, **kwargs):
    if created:
        message = (
            f'Заявка с сайта tdleningrad.ru:\n'
            f'<b>Имя</b>: {instance.name}\n'
            f'<b>Телефон</b>: {instance.phone}\n'
            f'<b>Дата создания</b>: {instance.created_at}'
        )
        # send_telegram_message(operator_id, message)
        send_telegram_message(admin_id, message)


@receiver(post_save, sender=FeedbackRequest)
def notify_operator_on_feedback_request(sender, instance, created, **kwargs):
    if created:
        message = (
            f'Заявка с сайта tdleningrad.ru:\n'
            f'<b>Имя</b>: {instance.name}\n'
            f'<b>Email</b>: {instance.email}\n'
            f'<b>Телефон</b>: {instance.phone}\n'
            f'<b>Товар</b>: {instance.product}\n'
            f'<b>Сообщение</b>: {instance.message}\n'
            f'<b>Дата создания</b>: {instance.created_at}'
        )
        # send_telegram_message(operator_id, message)
        send_telegram_message(admin_id, message)