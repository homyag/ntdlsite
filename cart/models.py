from django.db import models
from django.core.validators import MinValueValidator
from good.models import Product
from django.conf import settings


class Cart(models.Model):
    """Shopping cart for storing products before order completion"""
    session_id = models.CharField(max_length=255, null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['session_id']),
        ]

    def __str__(self):
        return f"Корзина {self.id} ({self.session_id})"

    def get_total_quantity(self):
        """Get total quantity of items in cart"""
        return sum(item.quantity for item in self.items.all())

    def get_total_cost(self):
        """Get total cost of all items in cart"""
        return sum(item.get_cost() for item in self.items.all())


class CartItem(models.Model):
    """Individual items in the shopping cart"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Товар в корзине"
        verbose_name_plural = "Товары в корзине"
        ordering = ['-added_at']
        unique_together = ['cart', 'product']
        indexes = [
            models.Index(fields=['cart', 'product']),
        ]

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        """Get cost of this item (price * quantity)"""
        return self.product.price * self.quantity


class Order(models.Model):
    """Customer orders"""
    ORDER_STATUS_CHOICES = (
        ('new', 'Новый'),
        ('processing', 'В обработке'),
        ('confirmed', 'Подтвержден'),
        ('shipping', 'Доставляется'),
        ('completed', 'Выполнен'),
        ('cancelled', 'Отменен'),
    )

    customer_name = models.CharField(max_length=255, verbose_name="Имя клиента")
    customer_email = models.EmailField(verbose_name="Email клиента")
    customer_phone = models.CharField(max_length=20, verbose_name="Телефон клиента")
    shipping_address = models.TextField(verbose_name="Адрес доставки")
    city = models.CharField(max_length=100, verbose_name="Город")
    status = models.CharField(max_length=20, choices=ORDER_STATUS_CHOICES,
                              default='new', verbose_name="Статус")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    comment = models.TextField(blank=True, null=True, verbose_name="Комментарий")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Общая стоимость")

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status']),
            models.Index(fields=['customer_email']),
        ]

    def __str__(self):
        return f"Заказ №{self.id} от {self.created_at.strftime('%d.%m.%Y')}"


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Товары в заказе"

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_cost(self):
        return self.price * self.quantity