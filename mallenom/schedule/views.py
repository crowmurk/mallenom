from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableMixin, Column
from django_filters.views import FilterView

from core.views import (
    ActionTableDeleteMixin,
    DeleteMessageMixin,
    SingleFormSetMixin,
)

from .models import Project, Assignment, ProjectAssignment, Absence
from .forms import (
    ProjectForm,
    AssignmentForm,
    ProjectAssignmentForm,
    ProjectAssignmentFormSet,
    AbsenceForm,
)
from .tables import (
    ProjectTable,
    AssignmentTable,
    ProjectAssignmentTable,
    AbsenceTable,
)
from .filters import (
    ProjectFilter,
    AssignmentFilter,
    ProjectAssignmentFilter,
    AbsenceFilter,
)

# Create your views here.

class ProjectList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Project
    table_class = ProjectTable
    filterset_class = ProjectFilter
    template_name = 'schedule/project_list.html'
    action_table_model = Project

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class ProjectCreate(CreateView):
    model = Project
    form_class = ProjectForm


class ProjectDetail(SingleTableMixin, ActionTableDeleteMixin, DetailView):
    model = Project
    form_class = ProjectForm
    table_class = ProjectAssignmentTable
    action_table_model = ProjectAssignment

    def get_table_kwargs(self):
        return {
            'exclude': ('project', 'delete', )
        }

    def get_table_data(self):
        return ProjectAssignment.objects.filter(
            project=self.object,
        )


class ProjectUpdate(UpdateView):
    model = Project
    form_class = ProjectForm


class ProjectDelete(DeleteMessageMixin, DeleteView):
    model = Project
    success_url = reverse_lazy('schedule:project:list')


class AssignmentList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Assignment
    table_class = AssignmentTable
    filterset_class = AssignmentFilter
    template_name = 'schedule/assignment_list.html'
    action_table_model = Assignment

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class AssignmentCreate(SingleFormSetMixin, CreateView):
    model = Assignment
    form_class = AssignmentForm
    formset = ProjectAssignmentFormSet


class AssignmentDetail(SingleTableMixin, ActionTableDeleteMixin, DetailView):
    model = Assignment
    form_class = AssignmentForm
    table_class = ProjectAssignmentTable
    action_table_model = ProjectAssignment

    def get_table_kwargs(self):
        return {
            'extra_columns': (('hours', Column(), ), ),
            'exclude': (
                'employee', 'employment',
                'start', 'end', 'delete',
            ),
        }

    def get_table_data(self):
        return ProjectAssignment.objects.filter(
            assignment=self.object,
        )


class AssignmentUpdate(SingleFormSetMixin, UpdateView):
    model = Assignment
    form_class = AssignmentForm
    formset = ProjectAssignmentFormSet

    def get_initial(self):
        initial = {'employee': self.object.employment.employee}
        initial.update(self.initial)
        return initial


class AssignmentDelete(DeleteMessageMixin, DeleteView):
    model = Assignment
    success_url = reverse_lazy('schedule:assignment:list')


class ProjectAssignmentList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = ProjectAssignment
    table_class = ProjectAssignmentTable
    filterset_class = ProjectAssignmentFilter
    template_name = 'schedule/projectassignment_list.html'
    action_table_model = ProjectAssignment

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class ProjectAssignmentCreate(CreateView):
    model = ProjectAssignment
    form_class = ProjectAssignmentForm


class ProjectAssignmentDetail(DetailView):
    model = ProjectAssignment
    form_class = ProjectAssignmentForm


class ProjectAssignmentUpdate(UpdateView):
    model = ProjectAssignment
    form_class = ProjectAssignmentForm


class ProjectAssignmentDelete(DeleteMessageMixin, DeleteView):
    model = ProjectAssignment
    success_url = reverse_lazy('schedule:projectassignment:list')


class AbsenceList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Absence
    table_class = AbsenceTable
    filterset_class = AbsenceFilter
    template_name = 'schedule/absence_list.html'
    action_table_model = Absence

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class AbsenceCreate(CreateView):
    model = Absence
    form_class = AbsenceForm


class AbsenceDetail(DetailView):
    model = Absence
    form_class = AbsenceForm


class AbsenceUpdate(UpdateView):
    model = Absence
    form_class = AbsenceForm

    def get_initial(self):
        initial = {'employee': self.object.employment.employee}
        initial.update(self.initial)
        return initial


class AbsenceDelete(DeleteMessageMixin, DeleteView):
    model = Absence
    success_url = reverse_lazy('schedule:absence:list')
