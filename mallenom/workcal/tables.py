from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import DayType, Day


class DayTypeTable(tables.Table):
    name = tables.LinkColumn(
        verbose_name=_('Type')
    )
    days_count = tables.Column(
        verbose_name=_("Days count"),
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = DayType
        fields = (
            'name',
            'hours',
            'css_class',
            'csv_mark',
            'days_count'
        )
        empty_text = _("There are no records available")


class DayTable(tables.Table):
    date = tables.LinkColumn()
    hours = tables.Column(
        accessor='day_type.hours',
    )
    day_type = tables.LinkColumn(
        verbose_name=_('Type'),
        accessor='day_type.name',
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Day
        fields = (
            'date',
            'hours',
            'day_type',
        )
        empty_text = _("There are no records available")
