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
        # 'seo_title': 'ТД Ленинградский — качественный бетон и смеси',
        # 'seo_description': 'Производство и доставка бетона высокого качества от ТД Ленинградский',
        # 'seo_keywords': 'бетон, бетонные смеси, ТД Ленинградский',
    }


def city_context(request):
    city_slug = request.session.get('city_slug')
    city_name = None
    if city_slug:
        city = City.objects.filter(slug=city_slug).first()
        if city:
            city_name = city.name
    return {
        'city_slug': city_slug,
        'city_name': city_name,
        # 'cities': City.objects.all() if not city_slug else None,
        'cities': City.objects.all(),
    }