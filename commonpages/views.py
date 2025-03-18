from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings

from good.models import Product, City, Category
from django.db.models import Q
from django.utils.formats import localize
from django.utils.numberformat import format

from good.models import City, Product
from .forms import CallbackRequestForm, FeedbackForm

import requests
import json
import logging

logger = logging.getLogger(__name__)


def index(request):
    data = {
        "title": "Производитель бетона и бетонных смесей ТД Ленинградский",
        "seo_title": "Производитель бетона и бетонных смесей ТД Ленинградский",
        'seo_description': 'ТД Ленинградский — ведущий производитель бетона и бетонных смесей в регионе.',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
    }
    return render(request, "commonpages/main.html", context=data)


def about(request):
    # city_slug = request.session.get('city_slug')
    data = {
        "title": "Бетонный завод ТД Ленинградский",
        "seo_title": "О компании ТД Ленинградский - производителе бетона и "
                     "бетонных смесей",
        'seo_description': 'Производитель бетона и бетонных смесей в регионе '
                           'деятельности - ТД Ленинградский',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        # 'city_slug': city_slug,
    }
    return render(request, "commonpages/about.html", context=data)


def contacts(request):
    # proucts = Product.objects.all()
    products = Product.objects.order_by('name').distinct('name')
    # city_slug = request.session.get('city_slug')
    data = {
        "title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        # "menu": menu,
        "seo_title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        'seo_description': 'Контакты бетонного завода ТД Ленинградский. '
                           'Продажа бетона и бетонных смесей от 1м3',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        'products': products,
        # 'city_slug': city_slug,
    }
    return render(request, "commonpages/contacts.html", context=data)


def services(request):
    # city_slug = request.session.get('city_slug')
    data = {
        "title": "Услуги производителя бетона и бетонных смесей ТД "
                 "Ленинградский",
        # "menu": menu,
        "seo_title": "Услуги производителя бетона и бетонных смесей ТД "
                     "Ленинградский",
        'seo_description': 'Доставка бетона и нерудных материалов '
                           'собственным автопарком или самовывозом с '
                           'производства',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        # 'city_slug': city_slug,
    }
    return render(request, "commonpages/services.html", context=data)


def delivery(request):
    data = {
        "title": "Калькулятор доставки бетона от завода ТД Ленинградский",
        "seo_title": "Калькулятор доставка бетона | Заказать бетон с доставкой",
        'seo_description': 'Закажите бетон с доставкой по доступной цене. '
                           'Рассчитайте стоимость доставки бетона миксером '
                           'онлайн с помощью Яндекс.Карт. Быстрая доставка, '
                           'качественный бетон, лучшие цены за 1 м³. '
                           'Свяжитесь с нами для заказа бетона с доставкой '
                           'уже сегодня',
        'seo_keywords': 'бетон цена за 1 м3 с доставкой, цена бетон с '
                        'доставкой за 1 м3, бетон с доставкой, доставка '
                        'бетона, бетон купить с доставкой цена, заказать '
                        'бетон с доставкой, бетон с доставкой цена, доставка'
                        ' бетона миксером, миксер бетона цена с доставкой, '
                        'заказать бетон с доставкой цена',
    }
    return render(request, "commonpages/delivery.html", context=data)


def concrete_calculator(request):
    # Контекстный процессор city_context добавляет city_slug в контекст
    # Нет необходимости добавлять его явно в context=data

    # Получаем город из контекстного процессора с помощью сессии
    city_slug = request.session.get('city_slug', 'mariupol')

    # Переменная для хранения продуктов
    concrete_products = []

    # Если город определен, получаем продукты
    if city_slug:
        # Получаем город
        try:
            city = City.objects.get(slug=city_slug)
            logger.info(f"Found city: {city.name} (ID: {city.id})")

            # Находим категорию бетона
            concrete_category = None
            try:
                concrete_category = Category.objects.get(slug='beton')
                logger.info(
                    f"Found category 'beton': {concrete_category.name} (ID: {concrete_category.id})")
            except Category.DoesNotExist:
                logger.warning("Category 'beton' not found")

            # Если категория найдена, ищем продукты
            products_list = []
            if concrete_category:
                # Получаем все продукты бетона в данной категории для выбранного города
                products = Product.objects.filter(
                    city=city,
                    category=concrete_category
                )
                logger.info(
                    f"Found {products.count()} products in category 'beton'")

                # Добавляем все продукты в список
                products_list.extend(list(products))

                # Если категория с бетоном имеет подкатегории, добавляем и их товары
                subcategories = Category.objects.filter(
                    parent=concrete_category)
                if subcategories.exists():
                    logger.info(f"Found {subcategories.count()} subcategories")

                    for subcat in subcategories:
                        logger.info(f"Processing subcategory: {subcat.name}")

                        subcat_products = Product.objects.filter(
                            city=city,
                            category=subcat
                        )

                        logger.info(
                            f"Found {subcat_products.count()} products in subcategory {subcat.name}")
                        products_list.extend(list(subcat_products))

            # Если категория не найдена или нет продуктов, ищем по названию
            if not products_list:
                logger.info(
                    "No products found in 'beton' category, searching by name...")

                # Ищем товары, в названии которых есть 'бетон' или 'цемент'
                name_products = Product.objects.filter(
                    city=city
                ).filter(
                    Q(name__icontains='бетон') | Q(name__icontains='цемент')
                )

                logger.info(
                    f"Found {name_products.count()} products by name search")
                products_list.extend(list(name_products))

            # Выводим общее количество найденных продуктов
            logger.info(f"Total products found: {len(products_list)}")

            # Преобразуем продукты в нужный формат
            for product in products_list:
                try:
                    price_float = float(product.price)

                    concrete_products.append({
                        'name': product.name,
                        'url': f"/catalog/{city_slug}/{product.category.slug}/{product.slug}/",
                        'price': price_float
                    })
                except (ValueError, TypeError, AttributeError) as e:
                    logger.error(
                        f"Error processing product {product.id} - {product.name}: {e}")

        except City.DoesNotExist:
            logger.error(f"City with slug '{city_slug}' not found")
            # Если город не найден, оставляем список пустым
            pass

        except Exception as e:
            logger.error(f"Unexpected error: {e}")

    # Если после всех поисков продуктов не найдено, добавляем тестовые продукты для бесперебойной работы
    if not concrete_products:
        logger.warning("No concrete products found, adding test products")
        concrete_products = [
            {
                'name': "Бетон М100",
                'url': f"/catalog/{city_slug}/beton/beton-m100/",
                'price': 40000.0
            },
            {
                'name': "Бетон М200",
                'url': f"/catalog/{city_slug}/beton/beton-m200/",
                'price': 45000.0
            },
            {
                'name': "Бетон М250",
                'url': f"/catalog/{city_slug}/beton/beton-m250/",
                'price': 50000.0
            },
            {
                'name': "Бетон М300",
                'url': f"/catalog/{city_slug}/beton/beton-m300/",
                'price': 55000.0
            },
            {
                'name': "Бетон М350",
                'url': f"/catalog/{city_slug}/beton/beton-m350/",
                'price': 60000.0
            },
        ]

    # Сериализуем список в JSON для безопасной передачи в JavaScript
    concrete_products_json = json.dumps(concrete_products)

    # Подготовка данных для контекста
    data = {
        "title": "Онлайн-калькулятор бетона. Расчет бетонной смеси в м3",
        "seo_title": "Расчет объема бетона онлайн | Онлайн-калькулятор бетона",
        'seo_description': 'Калькулятор для автоматического определения '
                           'необходимого объема бетона на основе ваших '
                           'данных. Не забудьте добавить запасный объем для '
                           'возможных потерь.',
        'seo_keywords': 'калькулятор бетона, бетонный калькулятор,'
                        'калькулятор бетона онлайн, бетонный калькулятор онлайн'
                        'калькулятор бетона м3',
        'concrete_products_json': concrete_products_json,
        'debug_concrete_count': len(concrete_products),
    }

    return render(request, "commonpages/concrete_calculator.html",
                  context=data)


def privacy(request):
    return render(request, "commonpages/privacy.html")


@require_POST
def submit_callback(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    if not recaptcha_response:
        return JsonResponse({'status': 'error', 'errors': {
            'recaptcha': 'Проверка reCAPTCHA не пройдена. Пожалуйста, попробуйте еще раз.'}})

    # Проверяем токен reCAPTCHA с помощью запроса к API Google
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
        'remoteip': request.META.get('REMOTE_ADDR')
    }

    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data=data)
        result = r.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'errors': {
            'recaptcha': 'Ошибка проверки reCAPTCHA. Пожалуйста, попробуйте позже.'}})

    if not result.get('success'):
        # Если проверка не пройдена, возвращаем ошибку
        return JsonResponse({'status': 'error', 'errors': {
            'recaptcha': 'Неверная reCAPTCHA. Пожалуйста, попробуйте еще раз.'}})

    # Если reCAPTCHA пройдена, продолжаем обработку формы
    form = CallbackRequestForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        # Преобразуем ошибки формы в список строк
        errors = {field: [str(error) for error in error_list] for
                  field, error_list in form.errors.items()}
        return JsonResponse({'status': 'error', 'errors': errors})


@require_POST
def submit_feedback(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    if not recaptcha_response:
        return JsonResponse({'status': 'error', 'errors': {
            'recaptcha': 'Проверка reCAPTCHA не пройдена. Пожалуйста, попробуйте еще раз.'}})

    # Проверяем токен reCAPTCHA с помощью запроса к API Google
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
        'remoteip': request.META.get('REMOTE_ADDR')
    }

    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify',
                          data=data)
        result = r.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'errors': {
            'recaptcha': 'Ошибка проверки reCAPTCHA. Пожалуйста, попробуйте позже.'}})

    if not result.get('success'):
        # Если проверка не пройдена, возвращаем ошибку
        return JsonResponse({'status': 'error', 'errors': {
            'recaptcha': 'Неверная reCAPTCHA. Пожалуйста, попробуйте еще раз.'}})

    # Если reCAPTCHA пройдена, продолжаем обработку формы
    form = FeedbackForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        # Преобразуем ошибки формы в список строк
        errors = {field: [str(error) for error in error_list] for
                  field, error_list in form.errors.items()}
        return JsonResponse({'status': 'error', 'errors': errors})


@require_POST
def set_city(request):
    selected_city_slug = request.POST.get('city_slug')
    if selected_city_slug and City.objects.filter(
            slug=selected_city_slug).exists():
        request.session['city_slug'] = selected_city_slug
    # Определяем URL для перенаправления обратно
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)
