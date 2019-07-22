from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class StaffingConfig(AppConfig):
    name = 'staffing'
    verbose_name = _('Staffing')
