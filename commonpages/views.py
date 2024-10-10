from django.http import HttpResponse
from django.shortcuts import render

menu = [
    {"title": "О компании", "url_name": "about"},
    {"title": "Контакты", "url_name": "contacts"},
    {"title": "Продукция", "url_name": "catalog"},
    {"title": "Услуги", "url_name": "services"},
    {"title": "Блог", "url_name": "blog"},
]


def index(request):
    data = {
        "title": "Главная страница",
        "menu": menu,
    }
    return render(request, "commonpages/main.html", context=data)


def about(request):
    data = {
        "title": "Производитель бетона и бетонных смесей ТД Ленинградский",
        "menu": menu,
    }
    return render(request, "commonpages/about.html", context=data)


def contacts(request):
    data = {
        "title": "Контакты",
        "menu": menu,
    }
    return render(request, "commonpages/contacts.html", context=data)


def services(request):
    data = {
        "title": "Услуги",
        "menu": menu,
    }
    return render(request, "commonpages/services.html", context=data)


def delivery(request):
    data = {
        "title": "Калькулятор доставки",
        "menu": menu,
    }
    return render(request, "commonpages/delivery.html", context=data)
