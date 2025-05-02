from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

from .models import Order


@receiver(post_save, sender=Order)
def notify_on_order_creation(sender, instance, created, **kwargs):
    """Send email notifications when an order is created"""
    if created:
        # Send email to admin
        send_admin_notification(instance)

        # Send confirmation to customer
        send_customer_confirmation(instance)


def send_admin_notification(order):
    """Send notification email to administrators"""
    subject = f'Новый заказ №{order.id} на сайте ТД Ленинградский'

    # Create HTML message
    html_message = render_to_string('cart/email/admin_notification.html', {
        'order': order,
        'order_items': order.items.all(),
        'site_url': settings.SITE_URL,
    })

    # Plain text version
    plain_message = strip_tags(html_message)

    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.ADMIN_EMAIL],
        html_message=html_message,
        fail_silently=False
    )


def send_customer_confirmation(order):
    """Send order confirmation to customer"""
    subject = f'Ваш заказ №{order.id} принят - ТД Ленинградский'

    # Create HTML message
    html_message = render_to_string('cart/email/customer_confirmation.html', {
        'order': order,
        'order_items': order.items.all(),
        'site_url': settings.SITE_URL,
    })

    # Plain text version
    plain_message = strip_tags(html_message)

    # Send email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[order.customer_email],
        html_message=html_message,
        fail_silently=False
    )