from django.utils.translation import ugettext_lazy as _

import django_filters as filters

from .models import Department, Position, Staffing


class DepartmentFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='icontains',
    )
    staff_units = filters.ChoiceFilter(
        label=_('Staff units'),
        empty_label=_('All'),
        choices=((0, _('Stale')), (1, _('Actual'))),
        method='staff_units_filter',
    )

    class Meta:
        model = Department
        fields = []

    def staff_units_filter(self, queryset, name, value):
        return queryset.filter(
            **{'staff_units_count__gt' if int(value) else 'staff_units_count': 0}
        )


class PositionFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='icontains',
    )
    staff_units = filters.ChoiceFilter(
        label=_('Staff units'),
        empty_label=_('All'),
        choices=((0, _('Stale')), (1, _('Actual'))),
        method='staff_units_filter',
    )

    class Meta:
        model = Position
        fields = []

    def staff_units_filter(self, queryset, name, value):
        return queryset.filter(
            **{'staff_units_count__gt' if int(value) else 'staff_units_count': 0}
        )


class StaffingFilter(filters.FilterSet):
    department = filters.CharFilter(
        label=_('Department'),
        field_name='department__name',
        lookup_expr='icontains',
    )
    position = filters.CharFilter(
        label=_('Position'),
        field_name='position__name',
        lookup_expr='icontains',
    )
    staff_units = filters.ChoiceFilter(
        label=_('Staff units'),
        empty_label=_('All'),
        choices=((0, _('Stale')), (1, _('Actual'))),
        method='staff_units_filter',
    )

    class Meta:
        model = Staffing
        fields = []

    def staff_units_filter(self, queryset, name, value):
        return queryset.filter(
            **{'count__gt' if int(value) else 'count': 0}
        )
