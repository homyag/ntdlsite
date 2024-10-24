from good.models import City


def default_context(request):
    return {
        'menu': [
            {'title': 'О компании', 'url_name': 'about'},
            {'title': 'Контакты', 'url_name': 'contacts'},
            {'title': 'Продукция', 'url_name': 'catalog'},
            {'title': 'Услуги', 'url_name': 'services'},
            {'title': 'Блог', 'url_name': 'blog'},
        ],
    }


def city_context(request):
    DEFAULT_CITY_SLUG = 'mariupol'
    city_slug = request.session.get('city_slug', DEFAULT_CITY_SLUG)
    city = City.objects.filter(slug=city_slug).first()
    if not city:
        city = City.objects.filter(slug=DEFAULT_CITY_SLUG).first()
    return {
        'city_slug': city.slug,
        'city_name': city.name,
        'cities': City.objects.all(),
        'city_slugs': list(City.objects.values_list('slug', flat=True)),
    }