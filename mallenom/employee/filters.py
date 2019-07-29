from django.db.models import Q
from django.utils.translation import ugettext_lazy as _

import django_filters as filters

from .models import Employee, Employment


class EmployeeFilter(filters.FilterSet):
    full_name = filters.CharFilter(
        label=_('Employee'),
        lookup_expr='icontains',
    )
    staff_units_count = filters.ChoiceFilter(
        label=_('Staff units'),
        empty_label=_('All'),
        choices=((0, _('Stale')), (1, _('Actual'))),
        method='count_filter',
    )

    class Meta:
        model = Employee
        fields = []

    def count_filter(self, queryset, name, value):
        return queryset.filter(
            **{'staff_units_count__gt' if int(value) else 'staff_units_count': 0}
        )


class EmploymentFilter(filters.FilterSet):
    number = filters.CharFilter(
        lookup_expr='iexact',
    )
    employee = filters.CharFilter(
        label=_('Employee'),
        method='employee_filter',
    )
    department = filters.CharFilter(
        label=_('Department'),
        field_name='staffing__department__name',
        lookup_expr='icontains',
    )
    position = filters.CharFilter(
        label=_('Position'),
        field_name='staffing__position__name',
        lookup_expr='icontains',
    )
    count = filters.ChoiceFilter(
        label=_('Staff units'),
        empty_label=_('All'),
        choices=((0, _('Stale')), (1, _('Actual'))),
        method='count_filter',
    )

    class Meta:
        model = Employment
        fields = []

    def count_filter(self, queryset, name, value):
        return queryset.filter(
            **{'count__gt' if int(value) else 'count': 0}
        )

    def employee_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                Q(employee__first_name__icontains=word) | Q(employee__middle_name__icontains=word) | Q(employee__last_name__icontains=word)
            )
        return queryset
