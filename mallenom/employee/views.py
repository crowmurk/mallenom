from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from core.views import (
    ActionTableDeleteMixin,
    DeleteMessageMixin,
    SingleFormSetMixin,
)

from .models import Employee, Employment
from .forms import (
    EmployeeForm,
    EmploymentForm,
    EmploymentFormSet
)
from .tables import EmployeeTable, EmploymentTable
from .filters import EmployeeFilter, EmploymentFilter

# Create your views here.

class EmployeeList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Employee
    table_class = EmployeeTable
    filterset_class = EmployeeFilter
    template_name = 'employee/employee_list.html'
    action_table_model = Employee

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class EmployeeCreate(SingleFormSetMixin, CreateView):
    model = Employee
    form_class = EmployeeForm
    formset = EmploymentFormSet


class EmployeeDetail(SingleTableMixin, ActionTableDeleteMixin, DetailView):
    model = Employee
    form_class = EmployeeForm
    table_class = EmploymentTable
    action_table_model = Employment

    def get_table_kwargs(self):
        return {
            'exclude': ('employee', 'delete', )
        }

    def get_table_data(self):
        return Employment.objects.filter(
            employee=self.object,
        )


class EmployeeUpdate(SingleFormSetMixin, UpdateView):
    model = Employee
    form_class = EmployeeForm
    formset = EmploymentFormSet


class EmployeeDelete(DeleteMessageMixin, DeleteView):
    model = Employee
    success_url = reverse_lazy('employee:employee:list')


class EmploymentList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Employment
    table_class = EmploymentTable
    filterset_class = EmploymentFilter
    template_name = 'employee/employment_list.html'
    action_table_model = Employment

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class EmploymentCreate(CreateView):
    model = Employment
    form_class = EmploymentForm


class EmploymentDetail(DetailView):
    model = Employment
    form_class = EmploymentForm


class EmploymentUpdate(UpdateView):
    model = Employment
    form_class = EmploymentForm


class EmploymentDelete(DeleteMessageMixin, DeleteView):
    model = Employment
    success_url = reverse_lazy('employee:employment:list')
