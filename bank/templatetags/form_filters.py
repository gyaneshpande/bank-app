from django import template
from django.forms import BaseForm

register = template.Library()

@register.filter
def addclass(field, class_attr):
    if isinstance(field, BaseForm):
        return field
    elif hasattr(field, 'field'):
        field.field.widget.attrs.update({'class': class_attr})
        return field
    else:
        raise TypeError("The provided value is not a form field.")