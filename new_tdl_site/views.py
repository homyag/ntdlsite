from django.http import HttpResponseNotFound
from django.shortcuts import render


def page_not_found(request, exception):
    return HttpResponseNotFound('Страница не найдена')
