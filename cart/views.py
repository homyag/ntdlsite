from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from django.urls import reverse

from good.models import Product
from .cart import SessionCart
from .forms import CartAddProductForm, OrderCreateForm
from .models import Cart, CartItem, Order, OrderItem

import uuid
import requests


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
    """Отображение формы оформления и обработка создания заказа"""
    session_cart = SessionCart(request)

    # Проверяем, пуста ли корзина
    if len(session_cart) == 0:
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)

        # Получаем токен reCAPTCHA
        recaptcha_token = request.POST.get('g-recaptcha-response', '')

        # Проверяем токен reCAPTCHA только если форма прошла другие проверки
        if form.is_valid():
            # Проверка reCAPTCHA v3
            if not recaptcha_token:
                form.add_error(None, "Пожалуйста, перезагрузите страницу и попробуйте снова.")
                return render(request, 'cart/checkout.html', {
                    'cart': session_cart,
                    'form': form,
                    'title': 'Оформление заказа - ТД Ленинградский',
                    'seo_title': 'Оформление заказа - ТД Ленинградский',
                    'seo_description': 'Оформление заказа на продукцию бетонного завода ТД Ленинградский.',
                    'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
                })

            recaptcha_valid, recaptcha_score = validate_recaptcha_v3(recaptcha_token)

            # Если проверка не пройдена
            if not recaptcha_valid:
                form.add_error(None, "Проверка безопасности не пройдена. Пожалуйста, попробуйте еще раз.")
                return render(request, 'cart/checkout.html', {
                    'cart': session_cart,
                    'form': form,
                    'title': 'Оформление заказа - ТД Ленинградский',
                    'seo_title': 'Оформление заказа - ТД Ленинградский',
                    'seo_description': 'Оформление заказа на продукцию бетонного завода ТД Ленинградский.',
                    'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
                })

            # Если низкий балл (вероятно бот)
            if recaptcha_score < 0.5:  # Можно настроить порог от 0.0 до 1.0
                form.add_error(None, "Подозрительная активность обнаружена. Пожалуйста, попробуйте еще раз позже.")
                return render(request, 'cart/checkout.html', {
                    'cart': session_cart,
                    'form': form,
                    'title': 'Оформление заказа - ТД Ленинградский',
                    'seo_title': 'Оформление заказа - ТД Ленинградский',
                    'seo_description': 'Оформление заказа на продукцию бетонного завода ТД Ленинградский.',
                    'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,
                })

            # Все проверки пройдены, создаём заказ
            order = form.save(commit=False)
            # Устанавливаем общую стоимость
            order.total_cost = session_cart.get_total_price()
            # Отключаем автоматическую отправку уведомлений
            order.save(send_notification=False)

            # Добавляем товары заказа
            for item in session_cart:
                if 'product' in item:
                    OrderItem.objects.create(
                        order=order,
                        product=item['product'],
                        price=item['price'],
                        quantity=item['quantity']
                    )

            # Отправляем уведомления после создания всех товаров
            from cart.signals import send_admin_notification, send_customer_confirmation
            send_admin_notification(order)
            send_customer_confirmation(order)

            # Очищаем корзину
            session_cart.clear()

            # Сохраняем ID заказа в сессии для страницы благодарности
            request.session['order_id'] = order.id

            # Перенаправляем на страницу успеха
            return redirect('cart:order_success')
    else:
        # Инициализация формы с данными пользователя, если они доступны
        form = OrderCreateForm()

    return render(request, 'cart/checkout.html', {
        'cart': session_cart,
        'form': form,
        'title': 'Оформление заказа - ТД Ленинградский',
        'seo_title': 'Оформление заказа - ТД Ленинградский',
        'seo_description': 'Оформление заказа на продукцию бетонного завода ТД Ленинградский.',
        'recaptcha_site_key': settings.RECAPTCHA_SITE_KEY,  # Добавляем ключ reCAPTCHA для фронтенда
    })


def validate_recaptcha_v3(token):
    """Проверка токена reCAPTCHA v3 с Google"""
    if not token:
        return False, 0.0

    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': token
    }

    try:
        response = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = response.json()

        success = result.get('success', False)
        score = result.get('score', 0.0)  # reCAPTCHA v3 возвращает оценку от 0.0 до 1.0

        return success, score
    except Exception as e:
        print(f"Ошибка при проверке reCAPTCHA: {e}")
        return False, 0.0


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