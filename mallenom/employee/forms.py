from django import forms
from django.forms import inlineformset_factory

from .models import Employee, Employment


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('positions', )


class EmploymentForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = '__all__'


EmploymentFormSet = inlineformset_factory(
    Employee,
    Employee.positions.through,
    form=EmploymentForm,
    can_delete=True,
    extra=0,
)
