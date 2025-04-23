from django import template
from django.db.models import Q

import good.views as views
from good.models import Category

register = template.Library()


@register.inclusion_tag('good/includes/list_categories.html')
def show_categories(city_slug, category_selected=0):
    categories = Category.objects.select_related('parent').filter(
        Q(parent__isnull=True) | Q(parent=2)
    ).exclude(name='Нерудные материалы').order_by('name')
    return {
        'categories': categories,
        'category_selected': category_selected,
        'city_slug': city_slug
    }

