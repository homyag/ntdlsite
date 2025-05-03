from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from commonpages.models import CallbackRequest, FeedbackRequest, Redirect


@admin.register(CallbackRequest)
class CallbackRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'created_at')


@admin.register(FeedbackRequest)
class FeedbackRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'product', 'message', 'created_at')
    search_fields = ('name', 'email', 'phone', 'product__name')
    readonly_fields = ('created_at',)

    # Настройка отображения формы редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'email', 'phone', 'product')
        }),
        ('Сообщение', {
            'fields': ('message',)
        }),
        ('Дополнительно', {
            'fields': ('created_at',)
        }),
    )


@admin.register(Redirect)
class RedirectAdmin(admin.ModelAdmin):
    list_display = ('old_path', 'new_path', 'is_active', 'created_at', 'test_redirect')
    list_filter = ('is_active', 'created_at')
    search_fields = ('old_path', 'new_path')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)

    def test_redirect(self, obj):
        return format_html(
            '<a href="{}" target="_blank">Тестировать редирект</a>',
            obj.old_path
        )
    test_redirect.short_description = _('Тест редиректа')