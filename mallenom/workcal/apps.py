from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class WorkCalConfig(AppConfig):
    name = 'workcal'
    verbose_name = _('Work calendar')
