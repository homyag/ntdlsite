from django import template

register = template.Library()

@register.filter
def item_range(value, arg):
    """
    Returns a range of numbers from value to arg
    """
    return range(int(value), int(arg))