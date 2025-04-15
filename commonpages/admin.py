from django.contrib import admin


from commonpages.models import CallbackRequest, FeedbackRequest


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