from django import forms
from django.utils.translation import gettext_lazy as _

import django_filters as filters

from .models import DayType, Day


class DayTypeFilter(filters.FilterSet):
    name = filters.CharFilter(
        label=_('Type'),
        lookup_expr='icontains',
    )
    hours = filters.NumberFilter()

    class Meta:
        model = DayType
        fields = []


class DayFilter(filters.FilterSet):
    date__gte = filters.DateFilter(
        label=_('After'),
        field_name='date',
        lookup_expr='gte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    date__lte = filters.DateFilter(
        label=_('Before'),
        field_name='date',
        lookup_expr='lte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    day_type = filters.ChoiceFilter(
        empty_label=_('All'),
        choices=DayType.objects.values_list('id', 'name'),
    )

    class Meta:
        model = Day
        fields = []
