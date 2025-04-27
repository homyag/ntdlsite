from good.models import City
from django.shortcuts import redirect
from django.core.cache import cache
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from .models import Redirect


# middleware, которое проверяет наличие выбранного города в сессии и
# добавляет его в запрос
class CityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        city_slug = request.session.get('city_slug')
        if not city_slug:
            request.cities = City.objects.all()
        else:
            request.city_slug = city_slug
        response = self.get_response(request)
        return response


class RedirectMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Пропускаем редиректы для админки
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Получаем редиректы из кэша
        redirects = cache.get('redirects')
        if redirects is None:
            redirects = {
                r.old_path: r.new_path
                for r in Redirect.objects.filter(is_active=True)
            }
            cache.set('redirects', redirects, 60 * 60)  # Кэшируем на 1 час

        # Нормализуем текущий путь
        path = request.path
        if not path.startswith('/'):
            path = '/' + path

        # Проверяем пути с разными вариантами окончания
        path_variants = [path]
        if path.endswith('/'):
            path_variants.append(path[:-1])
        else:
            path_variants.append(path + '/')

        # Проверяем все варианты пути
        for path_variant in path_variants:
            if path_variant in redirects:
                new_path = redirects[path_variant]
                # Если новый путь относительный, добавляем ведущий слеш
                if not new_path.startswith(('http://', 'https://', '/')):
                    new_path = '/' + new_path
                return redirect(new_path, permanent=True)

        return self.get_response(request)
