from django.contrib import admin
from .models import Cart, CartItem, Order, OrderItem


# Inline admin for CartItem
class CartItemInline(admin.TabularInline):
    model = CartItem
    raw_id_fields = ['product']
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'session_id', 'user_email', 'created_at', 'get_item_count', 'get_total_value']
    list_filter = ['created_at']
    inlines = [CartItemInline]
    search_fields = ['session_id', 'user_email']

    def get_item_count(self, obj):
        return obj.items.count()

    get_item_count.short_description = 'Количество товаров'

    def get_total_value(self, obj):
        return sum(item.get_cost() for item in obj.items.all())

    get_total_value.short_description = 'Общая стоимость'


# Inline admin for OrderItem
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    readonly_fields = ['price', 'get_cost']

    def get_cost(self, obj):
        return obj.get_cost()

    get_cost.short_description = 'Стоимость'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer_name', 'customer_email', 'customer_phone',
                    'city', 'status', 'created_at', 'total_cost']
    list_filter = ['created_at', 'status', 'city']
    search_fields = ['id', 'customer_name', 'customer_email', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at', 'total_cost']
    inlines = [OrderItemInline]
    fieldsets = (
        ('Информация о клиенте', {
            'fields': ('customer_name', 'customer_email', 'customer_phone')
        }),
        ('Информация о доставке', {
            'fields': ('city', 'shipping_address')
        }),
        ('Информация о заказе', {
            'fields': ('status', 'total_cost', 'created_at', 'updated_at', 'comment')
        }),
    )

    def get_readonly_fields(self, request, obj=None):
        # Make total_cost editable for new orders
        if obj is None:
            return ['created_at', 'updated_at']
        return self.readonly_fields

    actions = ['mark_as_processing', 'mark_as_confirmed', 'mark_as_shipping', 'mark_as_completed', 'mark_as_cancelled']

    @admin.action(description='Отметить как "В обработке"')
    def mark_as_processing(self, request, queryset):
        queryset.update(status='processing')

    @admin.action(description='Отметить как "Подтвержден"')
    def mark_as_confirmed(self, request, queryset):
        queryset.update(status='confirmed')

    @admin.action(description='Отметить как "Доставляется"')
    def mark_as_shipping(self, request, queryset):
        queryset.update(status='shipping')

    @admin.action(description='Отметить как "Выполнен"')
    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')

    @admin.action(description='Отметить как "Отменен"')
    def mark_as_cancelled(self, request, queryset):
        queryset.update(status='cancelled')