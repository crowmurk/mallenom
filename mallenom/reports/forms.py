from calendar import monthrange

from django import forms
from django.utils.translation import gettext_lazy as _


class ReportDownloadForm(forms.Form):
    report = forms.ChoiceField(
        required=True,
        choices=(
            # Результатом выбора должен быть метод ReportBuilder
            ('', '---------'),
            ('assignment_report', _("Employees' assignments")),
            ('assignment_matrix_report', _("Employees' assignments matrix")),
            ('assignment_matrix_report_xlsx', _("Employees' assignments matrix (Excel)")),
            ('assignment_hours_check_xlsx', _("Employees' work hours check")),
            ('index_of_labor_distribution_xlsx', _("Employees' indexes of labor distribution")),
            ('index_of_labor_distribution_per_project_xlsx', _("Employees' indexes of labor distribution per project")),
        ),
        label=_('Report'),
    )
    start = forms.DateField(
        required=True,
        label=_('Start date'),
    )
    end = forms.DateField(
        required=True,
        label=_('End date'),
    )
    orientation = forms.ChoiceField(
        required=True,
        choices=(
            ('portrait', _("Portrait")),
            ('landscape', _("Landscape")),
        ),
        label=_('Page orientation'),
    )

    def clean_start(self):
        if any(self.errors):
            return None

        start = self.cleaned_data['start']

        if start.weekday() == 0 or start.day == 1:
            return start

        raise forms.ValidationError(
            _("This value must be a Monday or first day of a month")
        )

    def clean_end(self):
        if any(self.errors):
            return None

        end = self.cleaned_data['end']
        month_length = monthrange(end.year, end.month)[1]

        if end.weekday() == 6 or end.day == month_length:
            return end

        raise forms.ValidationError(
            _("This value must be a Sunday or last day of a month")
        )

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
                    _('This value must be less or equal than %(end)s'),
                    code='invalid',
                    params={
                        'end': end,
                    },
                ),
            )
            return cleaned_data

        weekRange = start.weekday() == 0 and end.weekday() == 6
        monthRange = start.day == 1 and end.day == monthrange(
            end.year,
            end.month
        )[1]

        if not (weekRange or monthRange):
            self.add_error(
                None,
                forms.ValidationError(
                    _('Report can be weeks or months range only'),
                    code='invalid',
                ),
            )

        return cleaned_data
