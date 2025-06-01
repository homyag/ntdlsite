from django import template
from django.db.models import Q, Count

from good.models import Tag, Product

register = template.Library()


@register.inclusion_tag('good/includes/tag_filters.html')
def show_tag_filters(city_slug, current_category=None, selected_tag=None):
    """
    Отображает фильтр по тегам для данного города и категории
    """
    if not city_slug:
        return {'tags_by_category': {}}

    # Базовый queryset для тегов
    tags_query = Tag.objects.filter(
        is_active=True,
        products__city__slug=city_slug,
        products__on_stock=True
    )

    # Если указана категория, фильтруем теги по категории
    if current_category:
        tags_query = tags_query.filter(
            products__category=current_category
        )

    # Получаем теги с количеством товаров
    tags = tags_query.annotate(
        products_count=Count('products', filter=Q(
            products__city__slug=city_slug,
            products__on_stock=True
        ))
    ).filter(products_count__gt=0).distinct().order_by('sort_order', 'name')

    # Группируем теги по категориям
    tags_by_category = {}
    for tag in tags:
        tag_category = tag.category or 'Общие'
        if tag_category not in tags_by_category:
            tags_by_category[tag_category] = []
        tags_by_category[tag_category].append(tag)

    return {
        'tags_by_category': tags_by_category,
        'city_slug': city_slug,
        'selected_tag': selected_tag,
        'current_category': current_category
    }