from django.db import models
from django import forms
from django.conf import settings
from django.utils.translation import gettext_lazy as _

from staffing.models import Staffing

from .models import Employee, Employment


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('positions', )


class EmploymentForm(forms.ModelForm):
    class Meta:
        model = Employment
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """В форме должны отображаться только действующие штатные еденицы.
        """
        super().__init__(*args, **kwargs)
        self.fields['staffing'].queryset = Staffing.objects.filter(count__gt=0)

    def clean(self):
        """Колличество штатных едениц назначаемых сотруднику
        не должно превышать доступное по штатному расписанию.
        """
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        staffing = cleaned_data['staffing']
        staff_units = cleaned_data['count']
        staff_units_max = staffing.count

        # Занятое колличество штатных едениц (исключая указанные в форме)
        staff_units_holded = self._meta.model.objects.filter(
            staffing=staffing
        )
        if self.instance.pk:
            staff_units_holded = staff_units_holded.exclude(
                pk=self.instance.pk
            )
        staff_units_holded = staff_units_holded.aggregate(
            count_sum=models.functions.Coalesce(
                models.Sum('count'), 0
            )
        )['count_sum']

        staff_units_avalable = round(
            staff_units_max - staff_units_holded,
            settings.FLOAT_TOLERANCE,
        )

        if staff_units > staff_units_avalable:
            # Добавляем ошибку в форму
            message = _('This value must be less than or equal to %(count)s')
            self.add_error(
                'count',
                forms.ValidationError(
                    message,
                    code='invalid',
                    params={
                        'count': staff_units_avalable,
                    },
                ),
            )
        return cleaned_data


class BaseEmploymentFormSet(forms.BaseInlineFormSet):
    def clean(self):
        """Колличество штатных едениц назначаемых сотруднику
        не должно превышать доступное по штатному расписанию.
        """
        cleaned_data = super().clean()

        if any(self.errors):
            return cleaned_data

        validate_again = {}

        for form in self.forms:
            pk = form.instance.pk
            if not pk and not form.changed_data:
                # Новая, пустая форма
                continue
            staffing = form.cleaned_data['staffing']
            if self.can_delete and self._should_delete_form(form):
                # Форма назначена для удаления
                staff_units = 0
            else:
                staff_units = form.cleaned_data['count']

            # Добавляем данные формы для проверки
            if staffing in validate_again:
                validate_again[staffing]['staff_units'] += staff_units
                validate_again[staffing]['pks'].append(pk)
            else:
                validate_again[staffing] = {
                    'pks': [pk, ],
                    'staff_units': staff_units,
                }

        # Проверяем корректность назначения штатных едениц
        for staffing, data in validate_again.items():
            staff_units_max = staffing.count

            # Занятое колличество штатных едениц (исключая указанные в формах)
            staff_units_holded = self.model.objects.filter(
                staffing=staffing
            )
            pks = [pk for pk in data['pks'] if pk]
            if pks:
                staff_units_holded = staff_units_holded.exclude(
                    pk__in=pks
                )
            staff_units_holded = staff_units_holded.aggregate(
                count_sum=models.functions.Coalesce(
                    models.Sum('count'), 0
                )
            )['count_sum']

            staff_units_avalable = round(
                staff_units_max - staff_units_holded,
                settings.FLOAT_TOLERANCE,
            )

            staff_units = round(data['staff_units'], settings.FLOAT_TOLERANCE)

            if staff_units > staff_units_avalable:
                # Добавляем ошибку к форме
                message = _('%(units_count_name)s for all values'
                            ' %(staffing_name)s "%(staffing)s" must be less'
                            ' than or equal to %(count)s summary')
                self._non_form_errors.append(
                    forms.ValidationError(
                        message,
                        code='invalid',
                        params={
                            'units_count_name': self.model._meta.get_field(
                                'count',
                            ).verbose_name,
                            'staffing_name': self.model._meta.get_field(
                                'staffing',
                            ).verbose_name.lower(),
                            'staffing': staffing,
                            'count': staff_units_avalable,
                        },
                    )
                )
        return cleaned_data


EmploymentFormSet = forms.inlineformset_factory(
    Employee,
    Employee.positions.through,
    formset=BaseEmploymentFormSet,
    form=EmploymentForm,
    can_delete=True,
    extra=0,
)
