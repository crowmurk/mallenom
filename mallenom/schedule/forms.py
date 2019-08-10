import datetime

from django.db import models
from django import forms
from django.utils.translation import gettext_lazy as _

from workcal.models import Day

from .models import Project, Assignment, ProjectAssignment, Absence


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class AssignmentForm(forms.ModelForm):
    check_hours = forms.BooleanField(
        required=False,
        initial=True,
        label=_('Check hours'),
    )

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
    check_hours = forms.BooleanField(
        required=False,
        initial=True,
        label=_('Check hours'),
    )

    class Meta:
        model = ProjectAssignment
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        if not cleaned_data.get('check_hours'):
            return cleaned_data

        hours = cleaned_data['hours']
        assignment = cleaned_data['assignment']

        work_hours_max = Day.objects.get_work_hours_count(
            assignment.start,
            assignment.end,
        )

        hours_assigned = self._meta.model.objects.filter(
            assignment=assignment,
        )
        if self.instance.pk:
            hours_assigned = hours_assigned.exclude(
                pk=self.instance.pk
            )
        hours_assigned = hours_assigned.aggregate(
            hours=models.functions.Coalesce(
                models.Sum('hours'), 0
            ),
        )['hours']

        hours_available = work_hours_max - hours_assigned

        if hours > hours_available:
            self.add_error(
                'hours',
                forms.ValidationError(
                    _("This value must be less than or"
                      " equal to %(hours)s"),
                    code='invalid',
                    params={
                        'hours': hours_available,
                    },
                ),
            )
        return cleaned_data


class ProjectAssignmentFormsetForm(ProjectAssignmentForm):
    check_hours = None

    class Meta(ProjectAssignmentForm.Meta):
        pass


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


class BaseProjectAssignmentFormSet(forms.BaseInlineFormSet):
    def clean(self):
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        if not self.data.get('check_hours'):
            return cleaned_data

        hours = []
        assignment = self.instance

        for form in self.forms:
            if self.can_delete and self._should_delete_form(form):
                continue
            else:
                hours.append(form.cleaned_data['hours'])

        work_hours_max = Day.objects.get_work_hours_count(
            assignment.start,
            assignment.end,
        )

        if sum(hours) > work_hours_max:
            message = _('%(hours_name)s must be less than or equal to'
                        ' %(work_hours_max)s summary')
            self._non_form_errors.append(
                forms.ValidationError(
                    message,
                    code='invalid',
                    params={
                        'hours_name': self.model._meta.get_field(
                            'hours',
                        ).verbose_name,
                        'assignment_name': self.model._meta.get_field(
                            'assignment',
                        ).verbose_name.lower(),
                        'work_hours_max': work_hours_max,
                    },
                )
            )
        return cleaned_data


ProjectAssignmentFormSet = forms.inlineformset_factory(
    Assignment,
    Assignment.projects.through,
    formset=BaseProjectAssignmentFormSet,
    form=ProjectAssignmentFormsetForm,
    can_delete=True,
    extra=0,
)
