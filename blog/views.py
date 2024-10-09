from django.shortcuts import render


menu = [
    {"title": "О компании", "url_name": "about"},
    {"title": "Контакты", "url_name": "contacts"},
    {"title": "Продукция", "url_name": "catalog"},
    {"title": "Блог", "url_name": "blog"},
]


def blog(request):
    data = {
        'title': 'Блог',
        'menu': menu,
    }
    return render(request, 'blog/blog_main.html', context=data)