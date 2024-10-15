from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, get_list_or_404, \
    redirect
from django.template.loader import render_to_string

from .models import Product, Category, City


def product(request):
    city_slug = request.session.get('city_slug')
    city = None
    show_city_modal = False

    if city_slug:
        city = get_object_or_404(City, slug=city_slug)
        products = Product.objects.filter(city=city)
    else:
        # If city is not selected, show the modal
        products = Product.objects.all()
        show_city_modal = True
    # if not city_slug:
    #     return redirect('home')
    # city = get_object_or_404(City, slug=city_slug)
    # products = Product.objects.filter(city=city)
    data = {
        'title': 'Товарный каталог продукции ТД Ленинградский',
        'products': products,
        'seo_title': "Товарный каталог продукции ТД Ленинградский",
        'seo_description': "Продажа бетона и нерудных материалов от "
                           "производителя ТД Ленинградский",
        'seo_keywords': "купить бетон, продажа нерудных материалов, бетонный завод ТД Ленинградский",
        'city_slug': city_slug,
        'show_city_modal': show_city_modal,
        'city_name': city.name if city else None,
    }
    return render(request, 'good/products.html', context=data)


def show_product(request, category_slug, product_slug):
    city_slug = request.session.get('city_slug')
    if not city_slug:
        # Если город не выбран, перенаправляем на домашнюю страницу или
        # страницу выбора города
        return redirect('home')  # или 'set_city'

    city = get_object_or_404(City, slug=city_slug)
    category = get_object_or_404(Category,
                                 slug=category_slug)  # проверяем наличие категории
    good = get_object_or_404(Product, slug=product_slug, category=category,
                             city=city
                             )  #
    # находим продукт в этой категории

    data = {
        'title': good.name,
        'content': good.description,
        'category_selected': category_slug,
        'img': good.img.url if good.img else None,
        # Добавляем проверку наличия URL
        'property': good.product_card_property,
        'seo_title': good.meta_title,
        'seo_description': good.meta_description,
        'seo_keywords': good.meta_keywords,
        'city_slug': city_slug,
        'city_name': city.name,
    }
    return render(request, 'good/good.html', context=data)


def show_category(request, category_slug):
    city_slug = request.session.get('city_slug')

    show_city_modal = False
    city = None

    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Category.objects.filter(parent=category)

    if city_slug:
        city = get_object_or_404(City, slug=city_slug)
        products = Product.objects.filter(
            (Q(category=category) | Q(category__in=subcategories)) & Q(
                city=city)
        )
    else:
        # City not selected, show modal and possibly show no products
        products = Product.objects.none()
        show_city_modal = True

    data = {
        'title': f'Купить {category.name} от изготовителя продукции ТД Ленинградский',
        'products': products,
        'category_selected': category.pk,
        'description': category.description,
        'short_description': category.small_text_for_catalog,
        'seo_title': category.meta_title,
        'seo_description': category.meta_description,
        'seo_keywords': category.meta_keywords,
        'city_slug': city_slug,
        'city_name': city.name if city else None,
        'show_city_modal': show_city_modal,
    }
    return render(request, 'good/products.html', context=data)
