from calendar import monthrange

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_assignment_start(value):
    """Проверяет является ли дата
    понедельником или началом месяца.
    """
    if value.weekday() != 0 and value.day != 1:
        raise ValidationError(
            _("This date should be a Monday or first day of a month.")
        )

def validate_assignment_end(value):
    """Проверяет является ли дата
    воскресеньем или последним днем месяца.
    """
    month_length = monthrange(value.year, value.month)[1]

    if value.weekday() != 6 and value.day != month_length:
        raise ValidationError(
            _("This date should be a Sunday or last day of a month.")
        )
