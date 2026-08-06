from django import template

register = template.Library()

@register.filter
def id_number(value):
    """Format angka ke gaya Indonesia: 3359 -> 3.359"""
    try:
        value = int(value)
    except (TypeError, ValueError):
        return value
    return f"{value:,}".replace(",", ".")