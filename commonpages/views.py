from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from django.conf import settings

from good.models import City
from .forms import CallbackRequestForm

import requests


def index(request):
    city_slug = request.session.get('city_slug')
    data = {
        "title": "Производитель бетона и бетонных смесей ТД Ленинградский",
        "seo_title": "Производитель бетона и бетонных смесей ТД Ленинградский",
        'seo_description': 'ТД Ленинградский — ведущий производитель бетона и бетонных смесей в регионе.',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        'city_slug': city_slug,
    }
    return render(request, "commonpages/main.html", context=data)


def about(request):
    city_slug = request.session.get('city_slug')
    data = {
        "title": "О компании ТД Ленинградский - производителе бетона и "
                 "бетонных смесей",
        "seo_title": "О компании ТД Ленинградский - производителе бетона и "
                 "бетонных смесей",
        'seo_description': 'Ведущий производитель бетона и бетонных смесей в регионе деятельности - ТД Ленинградский',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        'city_slug': city_slug,
    }
    return render(request, "commonpages/about.html", context=data)


def contacts(request):
    city_slug = request.session.get('city_slug')
    data = {
        "title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        # "menu": menu,
        "seo_title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        'seo_description': 'Контакты бетонного завода ТД Ленинградский. '
                           'Продажа бетона и бетонных смесей от 1м3',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        'city_slug': city_slug,
    }
    return render(request, "commonpages/contacts.html", context=data)


def services(request):
    city_slug = request.session.get('city_slug')
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
        'city_slug': city_slug,
    }
    return render(request, "commonpages/services.html", context=data)


def delivery(request):
    city_slug = request.session.get('city_slug')
    data = {
        "title": "Калькулятор доставки бетона от завода ТД Ленинградский",
        # "menu": menu,
        "seo_title": "Калькулятор доставки бетона от завода ТД Ленинградский",
        'seo_description': 'Интерактивная карта доставки с калькулятором '
                           'стоимости доставки бетона по региону от ТД '
                           'Ленинградский',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
        'city_slug': city_slug,
    }
    return render(request, "commonpages/delivery.html", context=data)


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


def set_city(request):
    if request.method == 'POST':
        city_slug = request.POST.get('city_slug')
        city = City.objects.filter(slug=city_slug).first()
        if city:
            request.session['city_slug'] = city_slug
            return redirect(request.META.get('HTTP_REFERER', '/'))
        else:
            return JsonResponse({'error': 'Неверный выбор города'}, status=400)
    else:
        return JsonResponse({'error': 'Неверный метод запроса'}, status=400)


def change_city(request):
    # Удаляем city_slug из сессии
    if 'city_slug' in request.session:
        del request.session['city_slug']
    # Перенаправляем пользователя на главную страницу или другую страницу
    return redirect('home')