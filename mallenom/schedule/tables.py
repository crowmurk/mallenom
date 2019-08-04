from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import Project, Assignment, ProjectAssignment, Absence


class ProjectTable(tables.Table):
    name = tables.LinkColumn()
    delete = tables.CheckBoxColumn(accessor="pk")
    assignments_count = tables.Column(
        verbose_name=_("Assignments count"),
        footer=lambda table: _('Total: {}').format(
            sum(x.assignments_count for x in table.data)
        )
    )
    hours = tables.Column(
        verbose_name=_("Hours"),
        footer=lambda table: _('Total: {}').format(
            sum(x.hours for x in table.data)
        )
    )

    class Meta:
        model = Project
        fields = (
            'name',
            'status',
            'assignments_count',
            'hours',
        )
        empty_text = _("There are no records available")


class AssignmentTable(tables.Table):
    employee = tables.LinkColumn()
    projects = tables.ManyToManyColumn(
        linkify_item=(
            'schedule:project:detail',
            {'slug': tables.A('slug'), },
        )
    )
    hours = tables.LinkColumn(
        verbose_name=_("Hours"),
        footer=lambda table: _('Total: {}').format(
            sum(x.hours for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Assignment
        fields = (
            'employee',
            'projects',
            'start',
            'end',
            'hours',
        )
        empty_text = _("There are no records available")


class ProjectAssignmentTable(tables.Table):
    project = tables.LinkColumn()
    employee = tables.Column(
        linkify=(
            'employee:employee:detail',
            {'slug': tables.A('assignment.employee.slug'), },
        ),
        accessor="assignment.employee"
    )
    start = tables.Column(accessor="assignment.start")
    end = tables.Column(accessor="assignment.end")
    hours = tables.Column(
        linkify=(
            'schedule:assignment:detail',
            {'pk': tables.A('assignment.pk'), },
        ),
        footer=lambda table: _('Total: {}').format(
            sum(x.hours for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = ProjectAssignment
        fields = (
            'project',
            'employee',
            'start',
            'end',
            'hours',
        )
        empty_text = _("There are no records available")


class AbsenceTable(tables.Table):
    employee = tables.LinkColumn()
    hours = tables.LinkColumn(
        verbose_name=_("Hours"),
        footer=lambda table: _('Total: {}').format(
            sum(x.hours for x in table.data)
        )
    )
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Absence
        fields = (
            'employee',
            'start',
            'end',
            'hours',
        )
        empty_text = _("There are no records available")
