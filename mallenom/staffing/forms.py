from django import forms
from django.forms import inlineformset_factory

from .models import Department, Position, Staffing


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        exclude = ('positions', )


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = '__all__'


class StaffingForm(forms.ModelForm):
    class Meta:
        model = Staffing
        fields = '__all__'


StaffingFormSet = inlineformset_factory(
    Department,
    Department.positions.through,
    form=StaffingForm,
    can_delete=True,
    extra=0,
)
