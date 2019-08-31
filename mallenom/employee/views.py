from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.views.generic import (
    ListView,
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
from .utils import EmployeeContextMixin, EmploymentGetObjectMixin

# Create your views here.

class EmployeeList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Employee
    table_class = EmployeeTable
    table_pagination = False
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
    table_pagination = False
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
    table_pagination = False
    filterset_class = EmploymentFilter
    template_name = 'employee/employment_list.html'
    action_table_model = Employment

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }

class EmploymentListEmployee(
    EmployeeContextMixin,
    SingleTableMixin,
    ActionTableDeleteMixin,
    ListView,
):
    model = Employment
    table_class = EmploymentTable
    table_pagination = False
    template_name = 'employee/employment_list.html'
    action_table_model = Employment

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {
                'exclude': ('employee', )
            }
        return {
            'exclude': ('employee', 'delete', ),
        }

    def get_table_data(self):
        employee_slug = self.kwargs.get(self.employee_slug_url_kwarg)
        employee = Employee.objects.get(slug__iexact=employee_slug)
        return self.model.objects.filter(employee=employee)


class EmploymentCreate(
        EmployeeContextMixin,
        EmploymentGetObjectMixin,
        CreateView
):
    model = Employment
    form_class = EmploymentForm

    def get_initial(self):
        employee_slug = self.kwargs.get(
            self.employee_slug_url_kwarg)
        self.employee = get_object_or_404(
            Employee, slug__iexact=employee_slug)
        initial = {
            self.employee_context_object_name:
                self.employee,
        }
        initial.update(self.initial)
        return initial


class EmploymentDetail(
        EmployeeContextMixin,
        EmploymentGetObjectMixin,
        DetailView
):
    model = Employment
    form_class = EmploymentForm


class EmploymentUpdate(
        EmployeeContextMixin,
        EmploymentGetObjectMixin,
        UpdateView
):
    model = Employment
    form_class = EmploymentForm


class EmploymentDelete(
        EmployeeContextMixin,
        EmploymentGetObjectMixin,
        DeleteMessageMixin,
        DeleteView
):
    model = Employment

    def get_success_url(self):
        return self.object.employee.get_absolute_url()
