from decimal import Decimal
from django.conf import settings
from good.models import Product


class SessionCart:
    """Cart class that stores items in the session"""

    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Save an empty cart in the session
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        """
        Add a product to the cart or update its quantity.
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if override_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark the session as modified to make sure it gets saved"""
        self.session.modified = True

    def remove(self, product):
        """Remove a product from the cart."""
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def clear(self):
        """Remove cart from session."""
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        """
        Iterate over the items in the cart and get the products from the database.
        """
        product_ids = self.cart.keys()
        # Get product objects and add them to the cart
        products = Product.objects.filter(id__in=product_ids)

        # Создаем копию корзины для работы
        cart = self.cart.copy()

        # Создаем словарь продуктов по ID для быстрого доступа
        products_dict = {str(product.id): product for product in products}

        for product_id, item in cart.items():
            # Если продукт существует в базе данных
            if product_id in products_dict:
                # Добавляем объект продукта в словарь элемента корзины
                item['product'] = products_dict[product_id]
                # Преобразуем цену из строки в Decimal
                item['price'] = Decimal(item['price'])
                # Вычисляем общую стоимость
                item['total_price'] = item['price'] * item['quantity']
                # Возвращаем элемент
                yield item
            else:
                # Журналирование ошибки, если продукт не найден
                print(f"Предупреждение: продукт с ID {product_id} не найден в базе данных")

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate total cost of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def get_product_quantity(self, product_id):
        """Get quantity of a specific product in the cart."""
        product_id = str(product_id)
        if product_id in self.cart:
            return self.cart[product_id]['quantity']
        return 0

    def update_quantity(self, product, quantity):
        """Update product quantity in cart"""
        product_id = str(product.id)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = quantity
            self.save()