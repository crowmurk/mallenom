from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import Employee, Employment


class EmployeeTable(tables.Table):
    full_name = tables.LinkColumn(
        verbose_name=_('Employee'),
    )
    departments = tables.Column(
        verbose_name=_("Departments"),
    )
    positions_held = tables.Column(
        verbose_name=_("Positions held"),
    )
    staff_units_count = tables.Column(
        verbose_name=_("Staff units count"),
        footer=lambda table: _('Total: {}').format(
            sum(x.staff_units_count for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Employee
        fields = (
            'full_name',
            'departments',
            'positions_held',
            'staff_units_count',
        )
        empty_text = _("There are no records available")


class EmploymentTable(tables.Table):
    employee = tables.LinkColumn()
    department = tables.Column(
        linkify=(
            'staffing:department:detail',
            {'slug': tables.A('staffing.department.slug'), },
        ),
        accessor='staffing.department.name',
        verbose_name=_('Department'),
    )
    position = tables.Column(
        accessor='staffing.position.name',
        verbose_name=_('Position'),
    )
    count = tables.Column(
        footer=lambda table: _('Total: {}').format(
            sum(x.count for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Employment
        fields = (
            'number',
            'employee',
            'department',
            'position',
            'count',
        )
        empty_text = _("There are no records available")
