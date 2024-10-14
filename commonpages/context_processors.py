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