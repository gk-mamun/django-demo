# yourapp/templatetags/custom_filters.py
from django import template

register = template.Library()

@register.filter
def multiply_by_100(value):
    try:
        return value * 100
    except (TypeError, ValueError):
        return value

def getattr(obj, attr):
    return getattr(obj, attr, "N/A")