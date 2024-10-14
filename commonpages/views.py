from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.conf import settings

from .forms import CallbackRequestForm

import requests

# menu = [
#     {"title": "О компании", "url_name": "about"},
#     {"title": "Контакты", "url_name": "contacts"},
#     {"title": "Продукция", "url_name": "catalog"},
#     {"title": "Услуги", "url_name": "services"},
#     {"title": "Блог", "url_name": "blog"},
# ]


def index(request):
    data = {
        "title": "Производитель бетона и бетонных смесей ТД Ленинградский",
        # "menu": menu,
        "seo_title": "Производитель бетона и бетонных смесей ТД Ленинградский",
        'seo_description': 'ТД Ленинградский — ведущий производитель бетона и бетонных смесей в регионе.',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
    }
    return render(request, "commonpages/main.html", context=data)


def about(request):
    data = {
        "title": "О компании ТД Ленинградский - производителе бетона и "
                 "бетонных смесей",
        # "menu": menu,
        "seo_title": "О компании ТД Ленинградский - производителе бетона и "
                 "бетонных смесей",
        'seo_description': 'Ведущий производитель бетона и бетонных смесей в регионе деятельности - ТД Ленинградский',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
    }
    return render(request, "commonpages/about.html", context=data)


def contacts(request):
    data = {
        "title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        # "menu": menu,
        "seo_title": "Контакты бетонного завода ТД Ленинградский. Производство и отдел продаж",
        'seo_description': 'Контакты бетонного завода ТД Ленинградский. '
                           'Продажа бетона и бетонных смесей от 1м3',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
    }
    return render(request, "commonpages/contacts.html", context=data)


def services(request):
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
    }
    return render(request, "commonpages/services.html", context=data)


def delivery(request):
    data = {
        "title": "Калькулятор доставки бетона от завода ТД Ленинградский",
        # "menu": menu,
        "seo_title": "Калькулятор доставки бетона от завода ТД Ленинградский",
        'seo_description': 'Интерактивная карта доставки с калькулятором '
                           'стоимости доставки бетона по региону от ТД '
                           'Ленинградский',
        'seo_keywords': 'ТД Ленинградский, бетон, бетонные смеси, о компании',
    }
    return render(request, "commonpages/delivery.html", context=data)


# представление для обработки отправки формы Callback заявки через ajax
# @csrf_exempt
# def submit_callback(request):
#     if request.method == 'POST':
#         form = CallbackRequestForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return JsonResponse({'status': 'success'})
#         else:
#             return JsonResponse({'status': 'error', 'errors': form.errors})
#     return JsonResponse({'status': 'invalid request'}, status=400)

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