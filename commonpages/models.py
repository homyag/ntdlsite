from django.db import models
from good.models import Product
from django.utils.translation import gettext_lazy as _


class CallbackRequest(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.name} - {self.phone}'


class FeedbackRequest(models.Model):
    name = models.CharField(max_length=100, verbose_name="Имя")
    email = models.EmailField(verbose_name="Email")
    phone = models.CharField(max_length=20, verbose_name="Телефон")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL,
                                blank=True, null=True, verbose_name="Товар")
    message = models.TextField(verbose_name="Сообщение")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")

    def __str__(self):
        return f'{self.name} - {self.phone}'


class Redirect(models.Model):
    old_path = models.CharField(
        _('Старый путь'),
        max_length=255,
        db_index=True,
        help_text=_('Это должен быть абсолютный путь, исключая домен. Пример: "/search/".')
    )
    new_path = models.CharField(
        _('Новый путь'),
        max_length=255,
        help_text=_('Это может быть абсолютный путь или полный URL. Пример: "/search-new/" или "https://example.com/search/".')
    )
    is_active = models.BooleanField(
        _('Активен'),
        default=True,
        help_text=_('Определяет, будет ли редирект работать.')
    )
    created_at = models.DateTimeField(_('Создан'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Обновлен'), auto_now=True)

    class Meta:
        verbose_name = _('Редирект')
        verbose_name_plural = _('Редиректы')
        ordering = ['-created_at']
        unique_together = ['old_path']

    def __str__(self):
        return f"{self.old_path} → {self.new_path}"
