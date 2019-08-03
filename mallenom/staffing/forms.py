from django import forms
from django.db import models
from django.forms import inlineformset_factory
from django.conf import settings
from django.utils.translation import gettext_lazy as _

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

    def clean_count(self):
        if any(self.errors):
            return None

        count = self.cleaned_data['count']
        if self.instance.pk:
            staff_units_holded = self.instance.employments.aggregate(
                count_sum=models.functions.Coalesce(
                    models.Sum('count'), 0
                )
            )['count_sum']
            if round(staff_units_holded, settings.FLOAT_TOLERANCE) > count:
                message = _("This value must be greater than"
                            " or equal to {staff_units_holded}")
                raise forms.ValidationError(
                    message.format(
                        staff_units_holded=staff_units_holded,
                    )
                )
        return count


StaffingFormSet = inlineformset_factory(
    Department,
    Department.positions.through,
    form=StaffingForm,
    can_delete=True,
    extra=0,
)
