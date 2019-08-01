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

        start = cleaned_data.get('start', None)
        end = cleaned_data.get('end', None)

        if not start or not end:
            return

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

        start = cleaned_data.get('start', None)
        end = cleaned_data.get('end', None)

        if not start or not end:
            return

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


ProjectAssignmentFormSet = inlineformset_factory(
    Assignment,
    Assignment.projects.through,
    form=ProjectAssignmentForm,
    can_delete=True,
    extra=0,
)
