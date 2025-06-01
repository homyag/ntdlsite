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

        # Добавляем популярные теги в навигацию
        popular_tags = Tag.objects.filter(
            is_active=True,
            products__city__slug=city_slug,
            category='Применение'  # Только теги применения
        ).annotate(
            products_count=Count('products', filter=Q(products__city__slug=city_slug))
        ).filter(products_count__gt=0).distinct()[:3]  # Топ-3 тега

    else:
        # Если город не выбран, показываем все категории (как было раньше)
        categories = Category.objects.select_related('parent').filter(
            Q(parent__isnull=True) | Q(parent=2)
        ).exclude(name='Нерудные материалы').order_by('name')
        popular_tags = []

    # Единый return в конце функции
    return {
        'categories': categories,
        'popular_tags': popular_tags,  # Добавляем теги
        'category_selected': category_selected,
        'city_slug': city_slug
    }