from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from .models import Order

import logging

logger = logging.getLogger(__name__)


@receiver(post_save, sender=Order)
def notify_on_order_creation(sender, instance, created, **kwargs):
    send_notification = instance.__dict__.get('_send_notification', True)
    """Send email notifications when an order is created"""
    if created and send_notification:
        # Журналируем создание заказа
        logger.info(f"Создан новый заказ #{instance.id}")

        # Проверяем наличие товаров
        items_count = instance.items.count()
        logger.info(f"Заказ #{instance.id} содержит {items_count} товаров")

        if items_count == 0:
            logger.warning(f"ВНИМАНИЕ: Заказ #{instance.id} не содержит товаров!")

        # Перечисляем товары для отладки
        items = instance.items.all()
        for item in items:
            logger.info(f"Товар в заказе #{instance.id}: {item.quantity} x {item.product.name} (цена: {item.price})")

        # Send email to admin
        send_admin_notification(instance)

        # Send confirmation to customer
        send_customer_confirmation(instance)


def send_admin_notification(order):
    """Send notification email to administrators"""
    subject = f'Новый заказ №{order.id} на сайте ТД Ленинградский'

    # Принудительно загружаем товары заказа заранее
    order_items = list(order.items.select_related('product').all())

    # Журналируем количество товаров для отправки
    logger.info(f"Отправляем уведомление администратору о заказе #{order.id} с {len(order_items)} товарами")

    # Если товаров нет, пишем в журнал
    if not order_items:
        logger.warning(f"Пустой список товаров при отправке уведомления администратору о заказе #{order.id}")

    # Create HTML message with context and forced evaluation of queryset
    context = {
        'order': order,
        'order_items': order_items,
        'site_url': settings.SITE_URL,
    }

    html_message = render_to_string('cart/email/admin_notification.html', context)

    # Plain text version
    plain_message = strip_tags(html_message)

    # Send email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.ADMIN_EMAIL],
            html_message=html_message,
            fail_silently=False
        )
        logger.info(f"Уведомление администратору о заказе #{order.id} успешно отправлено")
    except Exception as e:
        logger.error(f"Ошибка при отправке уведомления администратору о заказе #{order.id}: {str(e)}")


def send_customer_confirmation(order):
    """Send order confirmation to customer"""
    subject = f'Ваш заказ №{order.id} принят - ТД Ленинградский'

    # Принудительно загружаем товары заказа заранее
    order_items = list(order.items.select_related('product').all())

    # Журналируем количество товаров для отправки
    logger.info(f"Отправляем подтверждение клиенту о заказе #{order.id} с {len(order_items)} товарами")

    # Если товаров нет, пишем в журнал
    if not order_items:
        logger.warning(f"Пустой список товаров при отправке подтверждения клиенту о заказе #{order.id}")

    # Create HTML message with context and forced evaluation of queryset
    context = {
        'order': order,
        'order_items': order_items,
        'site_url': settings.SITE_URL,
    }

    html_message = render_to_string('cart/email/customer_confirmation.html', context)

    # Plain text version
    plain_message = strip_tags(html_message)

    # Send email
    try:
        send_mail(
            subject=subject,
            message=plain_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[order.customer_email],
            html_message=html_message,
            fail_silently=False
        )
        logger.info(f"Подтверждение клиенту о заказе #{order.id} успешно отправлено")
    except Exception as e:
        logger.error(f"Ошибка при отправке подтверждения клиенту о заказе #{order.id}: {str(e)}")
