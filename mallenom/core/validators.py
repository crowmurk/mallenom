from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_monday(value):
    """Проверяет является ли дата понедельником
    """
    if value.weekday() != 0:
        raise ValidationError(
            _("This date should be a Monday.")
        )

def validate_sunday(value):
    """Проверяет является ли дата воскресеньем
    """
    if value.weekday() != 6:
        raise ValidationError(
            _("This date should be a Sunday.")
        )
