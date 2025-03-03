from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.conf import settings

from good.models import City, Product
from .forms import CallbackRequestForm, FeedbackForm

import requests


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
    proucts = Product.objects.all()
    # city_slug = request.session.get('city_slug')
    data = {
        "title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        # "menu": menu,
        "seo_title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        'seo_description': 'Контакты бетонного завода ТД Ленинградский. '
                           'Продажа бетона и бетонных смесей от 1м3',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        'products': proucts,
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
    }
    return render(request, "commonpages/concrete_calculator.html", context=data)


def privacy(request):
    return render(request, "commonpages/privacy.html")


@require_POST
def submit_callback(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    if not recaptcha_response:
        return JsonResponse({'status': 'error', 'errors': {'recaptcha': 'Проверка reCAPTCHA не пройдена. Пожалуйста, попробуйте еще раз.'}})

    # Проверяем токен reCAPTCHA с помощью запроса к API Google
    data = {
        'secret': settings.RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response,
        'remoteip': request.META.get('REMOTE_ADDR')
    }

    try:
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
        result = r.json()
    except requests.exceptions.RequestException as e:
        return JsonResponse({'status': 'error', 'errors': {'recaptcha': 'Ошибка проверки reCAPTCHA. Пожалуйста, попробуйте позже.'}})

    if not result.get('success'):
        # Если проверка не пройдена, возвращаем ошибку
        return JsonResponse({'status': 'error', 'errors': {'recaptcha': 'Неверная reCAPTCHA. Пожалуйста, попробуйте еще раз.'}})

    # Если reCAPTCHA пройдена, продолжаем обработку формы
    form = CallbackRequestForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        # Преобразуем ошибки формы в список строк
        errors = {field: [str(error) for error in error_list] for field, error_list in form.errors.items()}
        return JsonResponse({'status': 'error', 'errors': errors})


@require_POST
def submit_feedback(request):
    recaptcha_response = request.POST.get('g-recaptcha-response')
    if not recaptcha_response:
        return JsonResponse({'status': 'error', 'errors': {'recaptcha': 'Проверка reCAPTCHA не пройдена. Пожалуйста, попробуйте еще раз.'}})

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
        return JsonResponse({'status': 'error', 'errors': {'recaptcha': 'Ошибка проверки reCAPTCHA. Пожалуйста, попробуйте позже.'}})

    if not result.get('success'):
        # Если проверка не пройдена, возвращаем ошибку
        return JsonResponse({'status': 'error', 'errors': {'recaptcha': 'Неверная reCAPTCHA. Пожалуйста, попробуйте еще раз.'}})

    # Если reCAPTCHA пройдена, продолжаем обработку формы
    form = FeedbackForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({'status': 'success'})
    else:
        # Преобразуем ошибки формы в список строк
        errors = {field: [str(error) for error in error_list] for field, error_list in form.errors.items()}
        return JsonResponse({'status': 'error', 'errors': errors})



@require_POST
def set_city(request):
    selected_city_slug = request.POST.get('city_slug')
    if selected_city_slug and City.objects.filter(slug=selected_city_slug).exists():
        request.session['city_slug'] = selected_city_slug
    # Определяем URL для перенаправления обратно
    referer = request.META.get('HTTP_REFERER', '/')
    return redirect(referer)

