from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableMixin, LinkColumn
from django_filters.views import FilterView

from core.views import (
    ActionTableDeleteMixin,
    DeleteMessageMixin,
    SingleFormSetMixin,
)

from .models import Department, Position, Staffing
from .forms import (
    DepartmentForm,
    PositionForm,
    StaffingForm,
    StaffingFormSet
)
from .tables import DepartmentTable, PositionTable, StaffingTable
from .filters import DepartmentFilter, PositionFilter, StaffingFilter

# Create your views here.

class DepartmentList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Department
    table_class = DepartmentTable
    filterset_class = DepartmentFilter
    template_name = 'staffing/department_list.html'
    action_table_model = Department

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class DepartmentCreate(SingleFormSetMixin, CreateView):
    model = Department
    form_class = DepartmentForm
    formset = StaffingFormSet


class DepartmentDetail(SingleTableMixin, ActionTableDeleteMixin, DetailView):
    model = Department
    form_class = DepartmentForm
    table_class = StaffingTable
    action_table_model = Staffing

    def get_table_kwargs(self):
        return {
            'extra_columns': (('position', LinkColumn(), ), ),
            'exclude': ('department', 'delete', )
        }

    def get_table_data(self):
        return Staffing.objects.filter(
            department=self.object,
        )


class DepartmentUpdate(SingleFormSetMixin, UpdateView):
    model = Department
    form_class = DepartmentForm
    formset = StaffingFormSet


class DepartmentDelete(DeleteMessageMixin, DeleteView):
    model = Department
    success_url = reverse_lazy('staffing:department:list')


class PositionList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Position
    table_class = PositionTable
    filterset_class = PositionFilter
    template_name = 'staffing/position_list.html'
    action_table_model = Position

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class PositionCreate(CreateView):
    model = Position
    form_class = PositionForm


class PositionDetail(SingleTableMixin, ActionTableDeleteMixin, DetailView):
    model = Position
    form_class = PositionForm
    table_class = StaffingTable
    action_table_model = Staffing

    def get_table_kwargs(self):
        return {
            'exclude': ('position', 'delete', )
        }

    def get_table_data(self):
        return Staffing.objects.filter(
            position=self.object,
        )


class PositionUpdate(UpdateView):
    model = Position
    form_class = PositionForm


class PositionDelete(DeleteMessageMixin, DeleteView):
    model = Position
    success_url = reverse_lazy('staffing:position:list')


class StaffingList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Staffing
    table_class = StaffingTable
    filterset_class = StaffingFilter
    template_name = 'staffing/staffing_list.html'
    action_table_model = Staffing

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class StaffingCreate(CreateView):
    model = Staffing
    form_class = StaffingForm


class StaffingDetail(DetailView):
    model = Staffing
    form_class = StaffingForm


class StaffingUpdate(UpdateView):
    model = Staffing
    form_class = StaffingForm


class StaffingDelete(DeleteMessageMixin, DeleteView):
    model = Staffing
    success_url = reverse_lazy('staffing:staffing:list')
