from django import forms
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _

from .models import DayType, Day


class DayTypeForm(forms.ModelForm):
    class Meta:
        model = DayType
        fields = '__all__'


class DayForm(forms.ModelForm):
    class Meta:
        model = Day
        fields = '__all__'


class CalendarUploadForm(forms.Form):
    year = forms.IntegerField(
        required=True,
        validators=[
            MinValueValidator(1999),
        ],
        label=_('Year'),
        help_text=_('Pick a year to import'),
    )
    file = forms.FileField(
        required=True,
        label=_('File'),
        help_text=_('Pick a CSV file containing work calendar'),
    )

    def clean_file(self):
        if any(self.errors):
            return None

        file = self.cleaned_data['file']
        if not file.name.endswith('.csv'):
            raise forms.ValidationError(_('CSV file required'))
        return file
