from django.utils.translation import gettext_lazy as _

import django_tables2 as tables

from .models import Project, Assignment, ProjectAssignment, Absence


class ProjectTable(tables.Table):
    name = tables.LinkColumn()
    delete = tables.CheckBoxColumn(accessor="pk")

    class Meta:
        model = Project
        fields = (
            'name',
            'status',
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
    hours = tables.LinkColumn()
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
    hours = tables.LinkColumn()
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
