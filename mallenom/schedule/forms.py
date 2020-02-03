from django import forms
from django.db import models
from django.utils.translation import gettext_lazy as _

from employee.models import Employee, Employment
from workcal.models import Day

from .models import Project, Assignment, ProjectAssignment, Absence


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = '__all__'


class AssignmentForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        required=True,
        queryset=Employee.objects.filter(staff_units_count__gt=0),
        label=Employee._meta.verbose_name,
    )
    check_hours = forms.BooleanField(
        required=False,
        initial=True,
        label=_('Check hours'),
    )

    class Meta:
        model = Assignment
        fields = (
            'employee', 'employment',
            'start', 'end', 'check_hours',
        )
        exclude = ('projects', )

    def __init__(self, *args, **kwargs):
        """В форме должны отображаться только занимаемые должности.
        """
        super().__init__(*args, **kwargs)
        self.fields['employment'].queryset = Employment.objects.filter(
            count__gt=0,
        )

    def clean(self):
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        # Знанимаемая должность должна соответствовать сотруднику
        employee = cleaned_data['employee']
        employment = cleaned_data['employment']

        if employee != employment.employee:
            self.add_error(
                'employment',
                forms.ValidationError(
                    _('Selected %(employee_verbose)s does'
                      ' not hold this %(position_verbose)s'),
                    code='invalid',
                    params={
                        'employee_verbose': employee._meta.verbose_name.lower(),
                        'position_verbose': self._meta.model._meta.get_field(
                            'employment',
                        ).verbose_name.lower(),
                    },
                ),
            )

        # Назначение должно начинаться раньше чем заканчиваться
        start = cleaned_data['start']
        end = cleaned_data['end']

        if start > end:
            self.add_error(
                'start',
                forms.ValidationError(
                    _('This value must be less or equal than %(end)s'),
                    code='invalid',
                    params={
                        'end': end,
                    },
                ),
            )

        # Назначения должно быть в пределах недели и месяца
        start_week = start.isocalendar()[1]
        end_week = end.isocalendar()[1]

        if start.year != end.year or start.month != end.month or start_week != end_week:
            self.add_error(
                'start',
                forms.ValidationError(
                    _('%(model_verbose)s dates must be within same week and month'),
                    code='invalid',
                    params={
                        'model_verbose': self._meta.model._meta.verbose_name.lower(),
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

    def __init__(self, *args, **kwargs):
        """В форме должны отображаться только активыне проекты.
        """
        super().__init__(*args, **kwargs)
        self.fields['project'].queryset = Project.objects.filter(status=True)

    def clean(self):
        """Колличество часов в назначении не должно превышать максимально
        допустимое кол-во рабочих часов c учетом штатных едениц.
        """
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

        staff_units_count = assignment.employment.count

        hours_available = work_hours_max * staff_units_count - hours_assigned

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


class ProjectAssignmentFormSetForm(ProjectAssignmentForm):
    check_hours = None

    class Meta(ProjectAssignmentForm.Meta):
        pass


class AbsenceForm(forms.ModelForm):
    employee = forms.ModelChoiceField(
        required=True,
        queryset=Employee.objects.filter(staff_units_count__gt=0),
        label=Employee._meta.verbose_name,
    )

    class Meta:
        model = Absence
        fields = (
            'employee', 'employment',
            'start', 'end', 'hours', 'reason',
        )

    def __init__(self, *args, **kwargs):
        """В форме должны отображаться только занимаемые должности.
        """
        super().__init__(*args, **kwargs)
        self.fields['employment'].queryset = Employment.objects.filter(
            count__gt=0,
        )

    def clean(self):
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        # Занимаемая должность должна соответствовать сотруднику
        employee = cleaned_data['employee']
        employment = cleaned_data['employment']

        if employee != employment.employee:
            self.add_error(
                'employment',
                forms.ValidationError(
                    _('Selected %(employee_verbose)s does'
                      ' not hold this %(position_verbose)s'),
                    code='invalid',
                    params={
                        'employee_verbose': employee._meta.verbose_name.lower(),
                        'position_verbose': self._meta.model._meta.get_field(
                            'employment',
                        ).verbose_name.lower(),
                    },
                ),
            )

        # Отсутствие должно начинаться раньше чем заканчиваться
        start = cleaned_data['start']
        end = cleaned_data['end']

        if start > end:
            self.add_error(
                'start',
                forms.ValidationError(
                    _('This value must be less or equal %(end)s'),
                    code='invalid',
                    params={
                        'end': end,
                    },
                ),
            )

        # Отсутствие должно быть в пределах недели и месяца
        start_week = start.isocalendar()[1]
        end_week = end.isocalendar()[1]

        if start.year != end.year or start.month != end.month or start_week != end_week:
            self.add_error(
                'start',
                forms.ValidationError(
                    _('%(model_verbose)s dates must be within same week and month'),
                    code='invalid',
                    params={
                        'model_verbose': self._meta.model._meta.verbose_name.lower(),
                    },
                ),
            )

        # Кол-во часов не должно превышать допустимое
        # кол-во рабочих часов за период
        hours = cleaned_data['hours']
        hours_max = Day.objects.get_work_hours_count(
            start,
            end,
        ) * employment.count

        if hours > hours_max:
            self.add_error(
                'hours',
                forms.ValidationError(
                    _("This value must be less than or"
                      " equal to %(hours)s"),
                    code='invalid',
                    params={
                        'hours': hours_max,
                    },
                ),
            )

        # Отсутствия по занимаемой должности не должны пересекаться
        absences = self._meta.model.objects.filter(
            end__gte=start,
            start__lte=end,
            employment=employment,
        )
        if self.instance.pk:
            absences = absences.exclude(
                pk=self.instance.pk
            )

        if absences.exists():
            self.add_error(
                None,
                forms.ValidationError(
                    _("Range %(start_verbose)s - %(end_verbose)s overlapps"
                      " already existed %(absence_verbose)s with this"
                      " %(employment_verbose)s"),
                    code='invalid',
                    params={
                        'start_verbose': self._meta.model._meta.get_field(
                            'start',
                        ).verbose_name,
                        'end_verbose': self._meta.model._meta.get_field(
                            'end',
                        ).verbose_name,
                        'absence_verbose': self._meta.model._meta.verbose_name,
                        'employment_verbose': self._meta.model._meta.get_field(
                            'employment',
                        ).verbose_name,
                    },
                ),
            )

        return cleaned_data


class BaseProjectAssignmentFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """Кол-во часов не должно превышать допустимое
        кол-во рабочих часов за период.
        """
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        if self.instance.pk is None:
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

        staff_units_count = assignment.employment.count

        hours_available = work_hours_max * staff_units_count

        if sum(hours) > hours_available:
            message = _('%(hours_name)s must be less than or equal to'
                        ' %(hours_available)s summary')
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
                        'hours_available': hours_available,
                    },
                )
            )
        return cleaned_data


ProjectAssignmentFormSet = forms.inlineformset_factory(
    Assignment,
    Assignment.projects.through,
    formset=BaseProjectAssignmentFormSet,
    form=ProjectAssignmentFormSetForm,
    can_delete=True,
    extra=0,
)
