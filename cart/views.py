from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.conf import settings
from django.urls import reverse

from good.models import Product
from .cart import SessionCart
from .forms import CartAddProductForm, OrderCreateForm
from .models import Cart, CartItem, Order, OrderItem

import uuid


def cart_detail(request):
    """View for displaying the cart and its items"""
    session_cart = SessionCart(request)

    # Prepare the form to update quantities
    for item in session_cart:
        item['update_quantity_form'] = CartAddProductForm(
            initial={'quantity': item['quantity'],
                     'override': True})

    return render(request, 'cart/cart_detail.html', {
        'cart': session_cart,
        'title': 'Корзина - ТД Ленинградский',
        'seo_title': 'Корзина товаров - ТД Ленинградский',
        'seo_description': 'Просмотр и редактирование товаров в корзине перед оформлением заказа.',
    })


@require_POST
def cart_add(request, product_id):
    """Add product to cart or update its quantity"""
    product = get_object_or_404(Product, id=product_id)
    session_cart = SessionCart(request)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        session_cart.add(product=product,
                         quantity=cd['quantity'],
                         override_quantity=cd['override'])

    # If it's an AJAX request, return JSON response
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = len(session_cart)
        return JsonResponse({'cart_count': cart_count, 'success': True})

    # Otherwise redirect back to the product page or to the cart
    if 'next' in request.POST:
        return redirect(request.POST.get('next'))
    return redirect('cart:cart_detail')


@require_POST
def cart_remove(request, product_id):
    """Remove an item from the cart"""
    product = get_object_or_404(Product, id=product_id)
    session_cart = SessionCart(request)
    session_cart.remove(product)

    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = len(session_cart)
        cart_total = session_cart.get_total_price()
        return JsonResponse({
            'cart_count': cart_count,
            'cart_total': cart_total,
            'success': True
        })

    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, product_id):
    """Update the quantity of an item in the cart"""
    product = get_object_or_404(Product, id=product_id)
    session_cart = SessionCart(request)

    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        session_cart.add(product=product,
                         quantity=cd['quantity'],
                         override_quantity=cd['override'])

    # Return JSON response for AJAX requests
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        cart_count = len(session_cart)
        cart_total = session_cart.get_total_price()
        item_total = cd['quantity'] * product.price
        return JsonResponse({
            'cart_count': cart_count,
            'cart_total': cart_total,
            'item_total': item_total,
            'success': True
        })

    return redirect('cart:cart_detail')


def checkout(request):
    """Display checkout form and handle order creation"""
    session_cart = SessionCart(request)

    # Check if cart is empty
    if len(session_cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            # Create the order
            order = form.save(commit=False)
            # Calculate total cost
            order.total_cost = session_cart.get_total_price()
            # Установим параметр для предотвращения запуска сигнала
            order.save(send_notification=False)  # Добавим этот параметр в метод save

            # Add order items
            for item in session_cart:
                # Проверяем, что продукт существует
                if 'product' in item:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )
                else:
                    # Логирование ошибки, если продукт отсутствует
                    print(f"Ошибка: элемент корзины не содержит продукт: {item}")

            # Теперь, когда все товары созданы, вручную отправляем уведомления
            from cart.signals import send_admin_notification, send_customer_confirmation
            send_admin_notification(order)
            send_customer_confirmation(order)

            # Вывод информации о созданном заказе и его элементах для отладки
            print(f"Создан заказ #{order.id} с {order.items.count()} товарами")
            for item in order.items.all():
                print(f"- {item.quantity} x {item.product.name} (цена: {item.price})")

            # Clear the cart
            session_cart.clear()

            # Store order ID in session for thank you page
            request.session['order_id'] = order.id

            # Redirect to success page
            return redirect('cart:order_success')
    else:
        # Initialize form with user data if available
        form = OrderCreateForm()

    return render(request, 'cart/checkout.html', {
        'cart': session_cart,
        'form': form,
        'title': 'Оформление заказа - ТД Ленинградский',
        'seo_title': 'Оформление заказа - ТД Ленинградский',
        'seo_description': 'Оформление заказа на продукцию бетонного завода ТД Ленинградский.',
    })


def order_success(request):
    """Display order success page"""
    # Get order ID from session
    order_id = request.session.get('order_id')
    if not order_id:
        return redirect('home')

    order = get_object_or_404(Order, id=order_id)

    return render(request, 'cart/order_success.html', {
        'order': order,
        'title': 'Заказ успешно оформлен - ТД Ленинградский',
        'seo_title': 'Заказ успешно оформлен - ТД Ленинградский',
        'seo_description': 'Ваш заказ успешно оформлен и принят в обработку.',
    })


def cart_summary(request):
    """Return a JSON summary of the cart (for header display)"""
    session_cart = SessionCart(request)
    return JsonResponse({
        'count': len(session_cart),
        'total': str(session_cart.get_total_price())
    })