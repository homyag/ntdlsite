from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.template.context_processors import static
from django.urls import reverse

from .models import Product, Category, City


def product(request, city_slug):
    # Получение города
    city = get_object_or_404(City, slug=city_slug)

    # Получение продуктов с оптимизацией
    products = Product.objects.select_related(
        'category', 'city'
    ).only(
        'id', 'name', 'slug', 'price', 'product_card_description',
        'product_card_property', 'img', 'on_stock',
        'category__name', 'category__slug',
        'city__name', 'city__slug'
    ).filter(
        city=city,
        on_stock=True  # Добавляем фильтр по наличию товара
    )

    # Условное формирование заголовка
    if city.region:
        title = f"Товарный каталог продукции ТД Ленинградский в {city.region}: город {city.name}"
        seo_description = f"Бетон и нерудные материалы в {city.region}, город {city.name} от производителя | ТД Ленинградский"
    else:
        title = f"Товарный каталог продукции ТД Ленинградский в городе {city.name}"
        seo_description = f"Бетон и нерудные материалы от производителя город {city.name} | ТД Ленинградский"

    # Проверяем, пустая ли страница (нет товаров)
    empty_page = not products.exists()

    # Формирование данных для контекста
    data = {
        "title": title,
        "products": products,
        "seo_title": f"Товарный каталог продукции ТД Ленинградский в городе {city.name}",
        "seo_description": seo_description,
        "seo_keywords": "купить бетон, продажа нерудных материалов, бетонный завод ТД Ленинградский",
        "city_slug": city.slug,
        "city_name": city.name,
        "empty_page": empty_page,
        "breadcrumbs": [
            {"title": "Главная", "url": reverse("home")},
            {
                "title": f"Каталог {city.name}",
                "url": reverse("catalog", args=[city_slug]),
            },
        ],
    }

    # Рендеринг шаблона
    return render(request, "good/products.html", context=data)


def show_product(request, city_slug, category_slug, product_slug):
    city = get_object_or_404(City, slug=city_slug)
    category = get_object_or_404(Category, slug=category_slug)
    try:
        good = Product.objects.select_related(
            'category', 'city'
        ).get(
            slug=product_slug,
            category=category,
            city=city
        )
    except Product.DoesNotExist:
        good = None

    if good:
        related_goods = Product.objects.select_related(
            'category', 'city'
        ).only(
            'id', 'name', 'slug', 'img',
            'category__slug',
            'city__slug'
        ).filter(
            category=category,
            city=city,
            on_stock=True  # Только товары в наличии
        ).exclude(
            id=good.id
        )[:3]
        data = {
            "title": f"Купить {good.name} в городе {city.name}",
            "content": good.description,
            "category_selected": category.slug,
            "img": good.img.url if good.img else None,
            "property": good.product_card_property,
            "seo_title": good.meta_title,
            "seo_description": good.meta_description,
            "seo_keywords": good.meta_keywords,
            "city_slug": city.slug,
            "city_name": city.name,
            "good": good,
            "good_price": good.price,
            "related_goods": related_goods,
            "breadcrumbs": [
                {"title": "Главная", "url": reverse("home")},
                {
                    "title": "Каталог" + " " + city.name,
                    "url": reverse("catalog", args=[city_slug]),
                },
                {
                    "title": category.name,
                    "url": reverse("category", args=[city_slug, category_slug]),
                },
                {"title": good.name, "url": ""},  # Текущая страница
            ],
            # для schema.org
            "current_url": request.build_absolute_uri(),
            "site_name": "ТД Ленинградский",
            "currency": "RUB",
            "default_image": request.build_absolute_uri(
                static("images/mainpage/zavod.webp")
            ),
        }
    else:
        data = {
            "title": "Товар не найден",
            "city_slug": city.slug,
            "city_name": city.name,
            "breadcrumbs": [
                {"title": "Главная", "url": reverse("home")},
                {
                    "title": "Каталог" + " " + city.name,
                    "url": reverse("catalog", args=[city_slug]),
                },
            ],
        }
    return render(request, "good/good.html", context=data)


def show_category(request, city_slug, category_slug):
    city = get_object_or_404(City, slug=city_slug)
    category = get_object_or_404(Category, slug=category_slug)
    subcategories = Category.objects.filter(parent=category).values_list('id', flat=True)
    products = Product.objects.select_related(
        'category', 'city'
    ).only(
        'id', 'name', 'slug', 'price', 'product_card_description',
        'product_card_property', 'img', 'on_stock',
        'category__name', 'category__slug', 'category__id',
        'city__name', 'city__slug'
    ).filter(
        (Q(category=category) | Q(category__id__in=subcategories)) & Q(city=city),
        on_stock=True
    )

    # Получаем список названий товаров
    product_names = list(products.values_list("name", flat=True))

    if product_names:
        max_products = 10  # Максимальное количество товаров в описании
        if len(product_names) > max_products:
            displayed_products = product_names[:max_products]
            displayed_products.append("и другие")  # Добавляем фразу "и другие"
        else:
            displayed_products = product_names

        # Формируем строку с названиями товаров
        products_str = ", ".join(displayed_products)
    else:
        products_str = "Нет доступных товаров"

    # Формируем seo_description, учитывая ограничения по длине
    seo_description_base = (
        f"Купить {category.name} в городе {city.name}. "
        f"Каталог продукции ТД Ленинградский: {products_str}."
    )

    # Ограничиваем длину seo_description до 160 символов
    if len(seo_description_base) > 160:
        seo_description = seo_description_base[:157] + "..."
    else:
        seo_description = seo_description_base

    # Проверяем, пустая ли страница (нет товаров)
    empty_page = not products.exists()

    data = {
        "title": f"Купить {category.name} от производителя продукции ТД "
        f"Ленинградский в городе {city.name}",
        "products": products,
        "category_selected": category.pk,
        "description": category.description,
        "short_description": category.small_text_for_catalog,
        "seo_title": f"{category.meta_title} в городе {city.name}",
        "seo_description": seo_description,
        "seo_keywords": category.meta_keywords,
        "city_slug": city.slug,
        "city_name": city.name,
        "empty_page": empty_page,
        "breadcrumbs": [
            {"title": "Главная", "url": reverse("home")},
            {
                "title": "Каталог" + " " + city.name,
                "url": reverse("catalog", args=[city_slug]),
            },
            {
                "title": category.name,
                "url": reverse("category", args=[city_slug, category_slug]),
            },
        ],
    }
    return render(request, "good/products.html", context=data)
