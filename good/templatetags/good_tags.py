from django import template
from django.db.models import Q, Count

from good.models import Category, Product, Tag

register = template.Library()


@register.inclusion_tag('good/includes/list_categories.html')
def show_categories(city_slug, category_selected=0):
    if city_slug:
        # Находим категории, у которых есть товары в выбранном городе
        # 1. Сначала получаем все подходящие ID категорий
        category_ids_with_products = Product.objects.filter(
            city__slug=city_slug,
            on_stock=True  # Добавляем фильтр, чтобы показывать только категории с доступными товарами
        ).values_list('category_id', flat=True).distinct()

        # 2. Получаем родительские категории для найденных категорий
        parent_category_ids = Category.objects.filter(
            id__in=category_ids_with_products
        ).exclude(
            parent__isnull=True
        ).values_list('parent_id', flat=True).distinct()

        # 3. Объединяем ID категорий с товарами и ID родительских категорий
        all_relevant_category_ids = set(category_ids_with_products) | set(parent_category_ids)

        # 4. Получаем категории верхнего уровня и категории, которые имеют товары в выбранном городе
        categories = Category.objects.filter(
            Q(id__in=all_relevant_category_ids, parent__isnull=True) |
            Q(id__in=all_relevant_category_ids, parent_id=2)  # Сохраняем фильтр для категорий с parent=2
        ).exclude(
            name='Нерудные материалы'
        ).order_by('name')

        # Определяем, какую категорию показываем сейчас
        current_category = None
        if category_selected and category_selected != 0:
            try:
                current_category = Category.objects.get(id=category_selected)
            except Category.DoesNotExist:
                pass

        # Получаем релевантные теги в зависимости от выбранной категории
        popular_tags = get_relevant_tags_for_category(city_slug, current_category)

    else:
        # Если город не выбран, показываем все категории (как было раньше)
        categories = Category.objects.select_related('parent').filter(
            Q(parent__isnull=True) | Q(parent=2)
        ).exclude(name='Нерудные материалы').order_by('name')
        popular_tags = []

    # Единый return в конце функции
    return {
        'categories': categories,
        'popular_tags': popular_tags,
        'category_selected': category_selected,
        'city_slug': city_slug
    }


def get_relevant_tags_for_category(city_slug, current_category):
    """
    Получает релевантные теги для конкретной категории
    """
    if not current_category:
        # Если категория не выбрана, показываем общие популярные теги
        return Tag.objects.filter(
            is_active=True,
            products__city__slug=city_slug,
            category__in=['Общие', 'Популярные']  # Можно настроить под ваши нужды
        ).annotate(
            products_count=Count('products', filter=Q(products__city__slug=city_slug))
        ).filter(products_count__gt=0).distinct()[:4]

    # Маппинг категорий на типы тегов
    category_tag_mapping = {
        'Бетон': ['Применение', 'Марка'],
        'Асфальт': ['Тип асфальта', 'Применение'],
        'Щебень': ['Фракция', 'Порода'],
        'Песок': ['Тип песка', 'Применение'],
        'Цемент': ['Марка', 'Тип'],
        # Добавьте другие категории по необходимости
    }

    # Определяем типы тегов для текущей категории
    tag_categories = category_tag_mapping.get(current_category.name, ['Общие'])

    # Получаем теги, которые есть у товаров в данной категории и городе
    relevant_tags = Tag.objects.filter(
        is_active=True,
        products__city__slug=city_slug,
        products__category=current_category,
        category__in=tag_categories
    ).annotate(
        products_count=Count('products', filter=Q(
            products__city__slug=city_slug,
            products__category=current_category
        ))
    ).filter(products_count__gt=0).distinct().order_by('-products_count')[:5]

    return relevant_tags


@register.inclusion_tag('good/includes/application_filter.html')
def show_application_filter(city_slug, current_category_id=None):
    """
    Показывает фильтр по применению только для релевантных категорий
    """
    # Определяем категории, для которых показывать фильтр по применению
    categories_with_application_filter = ['Бетон', 'Асфальт', 'Цемент']

    current_category = None
    show_filter = False

    if current_category_id and current_category_id != 0:
        try:
            current_category = Category.objects.get(id=current_category_id)
            show_filter = current_category.name in categories_with_application_filter
        except Category.DoesNotExist:
            pass

    application_tags = []
    if show_filter and city_slug:
        # Получаем теги применения для текущей категории
        application_tags = Tag.objects.filter(
            is_active=True,
            category='Применение',
            products__city__slug=city_slug,
            products__category=current_category
        ).annotate(
            products_count=Count('products', filter=Q(
                products__city__slug=city_slug,
                products__category=current_category
            ))
        ).filter(products_count__gt=0).distinct().order_by('sort_order', 'name')

    return {
        'show_filter': show_filter,
        'application_tags': application_tags,
        'city_slug': city_slug,
        'current_category': current_category
    }