import datetime

from django.db import models
from django import forms
from django.http.request import QueryDict
from django.utils.translation import gettext_lazy as _

import django_filters as filters

from .models import Project, Assignment, ProjectAssignment, Absence


class ProjectFilter(filters.FilterSet):
    name = filters.CharFilter(
        lookup_expr='icontains',
    )
    status = filters.BooleanFilter(
        widget=forms.Select(
            choices=(
                ('', _('All')),
                ('0', _('Closed')),
                ('1', _('Active'))
            ),
        ),
    )

    class Meta:
        model = Project
        fields = []


class AssignmentFilter(filters.FilterSet):
    employee = filters.CharFilter(
        label=_('Employee'),
        method='employee_filter',
    )
    project = filters.CharFilter(
        label=_('Project'),
        field_name='projects__name',
        lookup_expr='icontains',
    )
    start__gte = filters.DateFilter(
        label=_('Starts after'),
        field_name='start',
        lookup_expr='gte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    end__lte = filters.DateFilter(
        label=_('Ends before'),
        field_name='end',
        lookup_expr='lte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    year_month = filters.CharFilter(
        label=_('Month/Year'),
        method='year_month_filter',
        widget=forms.TextInput(
            attrs={'placeholder': _('[MM/]YYYY')},
        ),
    )

    class Meta:
        model = Assignment
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        if data is None:
            today = datetime.date.today()
            data = QueryDict("year_month={}/{}".format(
                today.month,
                today.year,
            ))

        super(AssignmentFilter, self).__init__(data, *args, **kwargs)

    def employee_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                models.Q(employment__employee__last_name__icontains=word) |
                models.Q(employment__employee__first_name__icontains=word) |
                models.Q(employment__employee__middle_name__icontains=word)
            )
        return queryset

    def year_month_filter(self, queryset, name, value):
        try:
            value = list(map(int, value.split('/')))
            value.append(None)
            month, year, *_ = value
            if not year:
                year, month = month, year
        except ValueError:
            return queryset.none()

        if month:
            return queryset.filter(
                models.Q(start__month=month) & models.Q(start__year=year) |
                models.Q(end__month=month) & models.Q(end__year=year)
            )

        return queryset.filter(
            models.Q(start__year=year) | models.Q(end__year=year)
        )


class ProjectAssignmentFilter(filters.FilterSet):
    project = filters.CharFilter(
        label=_('Project'),
        field_name='project__name',
        lookup_expr='icontains',
    )
    employee = filters.CharFilter(
        label=_('Employee'),
        method='employee_filter',
    )
    start__gte = filters.DateFilter(
        label=_('Starts after'),
        field_name='assignment__start',
        lookup_expr='gte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    end__lte = filters.DateFilter(
        label=_('Ends before'),
        field_name='assignment__end',
        lookup_expr='lte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    year_month = filters.CharFilter(
        label=_('Month/Year'),
        method='year_month_filter',
        widget=forms.TextInput(
            attrs={'placeholder': _('[MM/]YYYY')},
        ),
    )

    class Meta:
        model = ProjectAssignment
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        if data is None:
            today = datetime.date.today()
            data = QueryDict("year_month={}/{}".format(
                today.month,
                today.year,
            ))

        super(ProjectAssignmentFilter, self).__init__(data, *args, **kwargs)

    def employee_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                models.Q(assignment__employment__employee__last_name__icontains=word) |
                models.Q(assignment__employment__employee__first_name__icontains=word) |
                models.Q(assignment__employment__employee__middle_name__icontains=word)
            )
        return queryset

    def year_month_filter(self, queryset, name, value):
        try:
            value = list(map(int, value.split('/')))
            value.append(None)
            month, year, *_ = value
            if not year:
                year, month = month, year
        except ValueError:
            return queryset.none()

        if month:
            return queryset.filter(
                models.Q(assignment__start__month=month) & models.Q(assignment__start__year=year) |
                models.Q(assignment__end__month=month) & models.Q(assignment__end__year=year)
            )

        return queryset.filter(
            models.Q(assignment__start__year=year) | models.Q(assignment__end__year=year)
        )


class AbsenceFilter(filters.FilterSet):
    employee = filters.CharFilter(
        label=_('Employee'),
        method='employee_filter',
    )
    start__gte = filters.DateFilter(
        label=_('Starts after'),
        field_name='start',
        lookup_expr='gte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    end__lte = filters.DateFilter(
        label=_('Ends before'),
        field_name='end',
        lookup_expr='lte',
        widget=forms.DateInput(
            attrs={'placeholder': _('MM/DD/YYYY')},
        ),
    )
    year_month = filters.CharFilter(
        label=_('Month/Year'),
        method='year_month_filter',
        widget=forms.TextInput(
            attrs={'placeholder': _('[MM/]YYYY')},
        ),
    )

    class Meta:
        model = Absence
        fields = []

    def __init__(self, data=None, *args, **kwargs):
        if data is None:
            today = datetime.date.today()
            data = QueryDict("year_month={}/{}".format(
                today.month,
                today.year,
            ))

        super(AbsenceFilter, self).__init__(data, *args, **kwargs)

    def employee_filter(self, queryset, name, value):
        for word in value.split():
            queryset = queryset.filter(
                models.Q(employee__last_name__icontains=word) |
                models.Q(employee__first_name__icontains=word) |
                models.Q(employee__middle_name__icontains=word)
            )
        return queryset

    def year_month_filter(self, queryset, name, value):
        try:
            value = list(map(int, value.split('/')))
            value.append(None)
            month, year, *_ = value
            if not year:
                year, month = month, year
        except ValueError:
            return queryset.none()

        if month:
            return queryset.filter(
                models.Q(start__month=month) & models.Q(start__year=year) |
                models.Q(end__month=month) & models.Q(end__year=year)
            )

        return queryset.filter(
            models.Q(start__year=year) | models.Q(end__year=year)
        )
