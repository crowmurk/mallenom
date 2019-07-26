from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import Department, Position, Staffing


class DepartmentTable(tables.Table):
    name = tables.LinkColumn()
    positions_count = tables.Column(
        verbose_name=_("Positions"),
    )
    staff_units = tables.Column(
        verbose_name=_("Staff Units"),
        footer=lambda table: _('Total: {}').format(
            sum(x.staff_units for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Department
        sequence = (
            'name',
            'positions_count',
            'staff_units'
        )
        exclude = ('id', 'slug', )
        empty_text = _("There are no records available")


class PositionTable(tables.Table):
    name = tables.LinkColumn()
    departments_count = tables.Column(
        verbose_name=_("Departments"),
    )
    staff_units = tables.Column(
        verbose_name=_("Staff Units"),
        footer=lambda table: _('Total: {}').format(
            sum(x.staff_units for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Position
        sequence = (
            'name',
            'departments_count',
            'staff_units',
        )
        exclude = ('id', 'slug', )
        empty_text = _("There are no records available")


class StaffingTable(tables.Table):
    department = tables.Column(
        linkify=(
            'staffing:department:detail',
            {
                'slug': tables.A('department.slug'),
            },
        ),
        accessor='department.name',
        verbose_name=_('Department'),
    )
    count = tables.Column(
        footer=lambda table: _('Total: {}').format(
            sum(x.count for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Staffing
        sequence = (
            'department',
            'position',
            'count',
        )
        exclude = ('id', )
        empty_text = _("There are no records available")
