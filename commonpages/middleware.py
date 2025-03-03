from good.models import City


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
