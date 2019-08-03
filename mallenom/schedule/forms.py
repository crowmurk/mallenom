import datetime

from django import forms
from django.forms import inlineformset_factory
from django.utils.translation import gettext_lazy as _

from .models import Project, Assignment, ProjectAssignment, Absence


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class AssignmentForm(forms.ModelForm):
    class Meta:
        model = Assignment
        exclude = ('projects', )

    def clean(self):
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        start = cleaned_data['start']
        end = cleaned_data['end']

        delta = end - start

        if start >= end:
            self.add_error(
                'start',
                forms.ValidationError(
                    _('Start date must be less than %(end)s'),
                    code='invalid',
                    params={
                        'end': end,
                    },
                ),
            )

        elif delta != datetime.timedelta(days=6):
            self.add_error(
                'end',
                forms.ValidationError(
                    _('There are seven days in a week, not %(delta)s'),
                    code='invalid',
                    params={
                        'delta': delta.days + 1,
                    },
                ),
            )
        return cleaned_data


class ProjectAssignmentForm(forms.ModelForm):
    class Meta:
        model = ProjectAssignment
        fields = '__all__'


class AbsenceForm(forms.ModelForm):
    class Meta:
        model = Absence
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        start = cleaned_data['start']
        end = cleaned_data['end']

        if start > end:
            self.add_error(
                'start',
                forms.ValidationError(
                    _('Start date must be less or equal %(end)s'),
                    code='invalid',
                    params={
                        'end': end,
                    },
                ),
            )
        return cleaned_data


ProjectAssignmentFormSet = inlineformset_factory(
    Assignment,
    Assignment.projects.through,
    form=ProjectAssignmentForm,
    can_delete=True,
    extra=0,
)
