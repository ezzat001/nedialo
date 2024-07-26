from django import template

register = template.Library()

@register.filter
def format_float(value):
    if isinstance(value, float) and value.is_integer():
        return int(value)
    return value



@register.filter
def count_services(queryset):
    return queryset.count()