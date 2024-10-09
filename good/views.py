from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404
from django.template.loader import render_to_string

from .models import Product, Category

menu = [
    {"title": "О компании", "url_name": "about"},
    {"title": "Контакты", "url_name": "contacts"},
    {"title": "Продукция", "url_name": "catalog"},
    {"title": "Услуги", "url_name": "services"},
    {"title": "Блог", "url_name": "blog"},
]


def product(request):
    products = get_list_or_404(Product)
    data = {
        'title': 'Товарный каталог продукции ТД Ленинградский',
        'menu': menu,
        'products': products,
    }
    return render(request, 'good/products.html', context=data)


def show_product(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)  # проверяем наличие категории
    good = get_object_or_404(Product, slug=product_slug, category=category)  #
    # находим продукт в этой категории

    data = {
        'title': good.name,
        'menu': menu,
        'content': good.description,
        'category_selected': category_slug,
        'img': good.img.url if good.img else None,  # Добавляем проверку наличия URL
    }
    return render(request, 'good/good.html', context=data)


def show_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Category.objects.filter(parent=category)
    # products = Product.objects.filter(category=category)

    products = Product.objects.filter(
        Q(category=category) | Q(category__in=subcategories)
    )

    data = {
        'title': f'Категория: {category.name}',
        'menu': menu,
        'products': products,
        # 'category_selected': category_slug,
        'category_selected': category.pk,
        'description': category.description,
    }
    return render(request, 'good/products.html', context=data)

