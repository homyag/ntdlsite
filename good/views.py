from django.db.models import Q
from django.shortcuts import render, get_object_or_404

from .models import Product, Category, City


def product(request, city_slug):
    city = get_object_or_404(City, slug=city_slug)
    products = Product.objects.filter(city=city)
    data = {
        'title': 'Товарный каталог продукции ТД Ленинградский в городе ' +
                 city.name,
        'products': products,
        'seo_title': "Товарный каталог продукции ТД Ленинградский в городе " +
                     city.name,
        'seo_description': "Продажа бетона и нерудных материалов от "
                           "производителя ТД Ленинградский в городе " + city.name,
        'seo_keywords': "купить бетон, продажа нерудных материалов, "
                        "бетонный завод ТД Ленинградский",
        'city_slug': city.slug,
        'city_name': city.name,
    }
    return render(request, 'good/products.html', context=data)


def show_product(request, city_slug, category_slug, product_slug):
    city = get_object_or_404(City, slug=city_slug)
    category = get_object_or_404(Category, slug=category_slug)
    try:
        good = Product.objects.get(slug=product_slug, category=category,
                                   city=city)
    except Product.DoesNotExist:
        good = None

    if good:
        data = {
            'title': f'Купить {good.name} в городе {city.name}',
            'content': good.description,
            'category_selected': category.slug,
            'img': good.img.url if good.img else None,
            'property': good.product_card_property,
            'seo_title': good.meta_title,
            'seo_description': good.meta_description,
            'seo_keywords': good.meta_keywords,
            'city_slug': city.slug,
            'city_name': city.name,
            'good': good,
        }
    else:
        data = {
            'title': 'Товар не найден',
            'city_slug': city.slug,
            'city_name': city.name,
        }
    return render(request, 'good/good.html', context=data)


def show_category(request, city_slug, category_slug):
    city = get_object_or_404(City, slug=city_slug)
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Category.objects.filter(parent=category)
    products = Product.objects.filter(
        (Q(category=category) | Q(category__in=subcategories)) & Q(city=city)
    )
    data = {
        'title': f'Купить {category.name} от производителя продукции ТД '
                 f'Ленинградский в городе {city.name}',
        'products': products,
        'category_selected': category.pk,
        'description': category.description,
        'short_description': category.small_text_for_catalog,
        'seo_title': category.meta_title,
        'seo_description': category.meta_description,
        'seo_keywords': category.meta_keywords,
        'city_slug': city.slug,
        'city_name': city.name,
    }
    return render(request, 'good/products.html', context=data)
