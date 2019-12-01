from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views import View

from employee.models import Employee, Employment

# Create your views here.

class EmploymentListEmployee(View):
    def get(self, request, *args, **kwargs):
        """Возвращает response c JSON содержащим
        все записи о должностях сотрудника.
        """
        employee_pk = kwargs.get('pk')
        employee = get_object_or_404(
            Employee,
            pk=employee_pk,
        )
        employments = Employment.objects.filter(
            employee=employee,
            count__gt=0,
        )
        json_employments = serializers.serialize(
            "json",
            employments,
        )
        return HttpResponse(
            json_employments,
            content_type="application/json; encoding=utf-8",
        )
