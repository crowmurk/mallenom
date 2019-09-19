from django import template
from django.core.exceptions import FieldDoesNotExist

register = template.Library()

@register.filter
def verbose_name(obj):
    """Фильтр получает verbose_name модели
    """
    try:
        return getattr(obj._meta, 'verbose_name', '')
    except AttributeError:
        return ''


@register.filter
def verbose_name_plural(obj):
    """Фильтр получает verbose_name_plural модели
    """
    try:
        return getattr(obj._meta, 'verbose_name_plural', '')
    except AttributeError:
        return ''


@register.simple_tag
def field_verbose_name(obj, field):
    """Тег получает verbose_name поля заданой модели
    """
    try:
        field = obj._meta.get_field(field)
    except (FieldDoesNotExist, AttributeError):
        return ''

    if hasattr(field, 'verbose_name'):
        # Обычное поле или RelationField forward
        return getattr(field, 'verbose_name', '')
    # RelationField reverse
    return getattr(field.related_model._meta, 'verbose_name_plural', '')


@register.filter
def form_field_class_name(obj):
    """Фильтр получает имя класса поля формы
    """
    try:
        return obj.field.widget.__class__.__name__
    except AttributeError:
        return ''
