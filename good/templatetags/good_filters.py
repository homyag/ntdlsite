from django import template
import re

register = template.Library()


@register.filter
def format_property(property_line):
    """
    Форматирует строку свойства товара, добавляя HTML-теги для стилизации

    Например, "Класс: B15" превращается в "<strong>Класс:</strong> B15"
    """
    # Пытаемся найти разделитель между именем и значением свойства
    match = re.match(r'^([^:]+):(.*?)$', property_line)

    if match:
        property_name = match.group(1).strip()
        property_value = match.group(2).strip()
        return f'<strong>{property_name}:</strong> {property_value}'
    else:
        return property_line