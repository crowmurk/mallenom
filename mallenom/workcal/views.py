import datetime

from django.forms.models import model_to_dict
from django.contrib import messages
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DetailView,
    UpdateView,
    DeleteView
)
from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from django_tables2 import SingleTableMixin
from django_filters.views import FilterView

from core.views import (
    ActionTableDeleteMixin,
    DeleteMessageMixin,
)
from core.logger import log

from .models import DayType, Day
from .forms import DayTypeForm, DayForm, CalendarUploadForm
from .tables import DayTypeTable, DayTable
from .filters import DayTypeFilter, DayFilter
from .utils import WorkCalendarParser

# Create your views here.

class DayTypeList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = DayType
    table_class = DayTypeTable
    table_pagination = False
    filterset_class = DayTypeFilter
    template_name = 'workcal/daytype_list.html'
    action_table_model = DayType
    table_pagination = False

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class DayTypeCreate(CreateView):
    model = DayType
    form_class = DayTypeForm


class DayTypeDetail(DetailView):
    model = DayType


class DayTypeUpdate(UpdateView):
    model = DayType
    form_class = DayTypeForm


class DayTypeDelete(DeleteMessageMixin, DeleteView):
    model = DayType
    success_url = reverse_lazy('workcal:daytype:list')


class DayList(SingleTableMixin, ActionTableDeleteMixin, FilterView):
    model = Day
    table_class = DayTable
    table_pagination = False
    filterset_class = DayFilter
    template_name = 'workcal/day_list.html'
    action_table_model = Day

    def get_table_kwargs(self):
        if self.request.user.is_superuser:
            return {}
        return {
            'exclude': ('delete', ),
        }


class DayCreate(CreateView):
    model = Day
    form_class = DayForm

    def get_initial(self):
        initial = super().get_initial()

        if self.request.method == 'GET':
            date = self.request.GET.get('date', '')
            try:
                date = datetime.date.fromisoformat(date)
            except ValueError:
                date = None
            except AttributeError:
                try:
                    date = datetime.date(*map(int, date.split('-')))
                except ValueError:
                    date = None

        if date is not None:
            initial.update({'date': date})

        return initial


class DayDetail(DetailView):
    model = Day


class DayUpdate(UpdateView):
    model = Day
    form_class = DayForm


class DayDelete(DeleteMessageMixin, DeleteView):
    model = Day
    success_url = reverse_lazy('workcal:day:list')


class CalendarDetail(TemplateView):
    template_name = "workcal/calendar_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = context.get('year')

        if not year or not datetime.MINYEAR <= year <= datetime.MAXYEAR:
            year = datetime.date.today().year
            context['year'] = year

        return context


class CalendarUpload(FormView):
    template_name = 'workcal/calendar_upload_form.html'
    form_class = CalendarUploadForm
    success_url = reverse_lazy('workcal:calendar:current')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST, request.FILES)

        if not form.is_valid():
            return self.form_invalid(form)

        csv_file = request.FILES["file"]

        # Файл слишком большой
        if csv_file.multiple_chunks():
            form.add_error(
                'file',
                _("Uploaded file is too big ({0:.2f} MB).").format(
                    csv_file.size / (1000 * 1000),
                ),
            )
            return self.form_invalid(form)

        # Загрузка и обработка данных
        try:
            data = WorkCalendarParser(
                csv_file.read().decode("utf-8"),
            ).get_days_list(form.cleaned_data['year'])
        except Exception as error:
            form.add_error(
                'file',
                _("Parsing error ({type}): {error}").format(
                    error=error,
                    type=type(error).__name__,
                ))
            return self.form_invalid(form)

        # Нет данных для обработки
        if not data:
            form.add_error(
                '__all__',
                _("Nothing to upload: data set is empty"),
            )
            return self.form_invalid(form)

        # Переходим к импорту данных
        return self.form_valid(form, data)

    def form_valid(self, form, data):
        # Сущесвующие в базе дни
        days_exists = list(Day.objects.filter(
            date__year=form.cleaned_data['year'],
        ).values_list('date', flat=True))

        # Дни для добавления
        days_raw = filter(
            lambda x: x['date'] not in days_exists,
            data,
        )

        log.info("Starting import CSV...")
        errors = False

        for day_raw in days_raw:
            # Добавляем дни
            day_form = DayForm(day_raw)
            if day_form.is_valid():
                day_form.save()
            else:
                errors = True
                log.error("{}: {} ".format(
                    model_to_dict(day_form.instance),
                    day_form.errors.as_data(),
                ))

        if errors:
            log.error("CSV import finished with errors")
            messages.error(
                self.request,
                _("CSV import finished with errors (see more in logs)"),
            )
        else:
            log.info("CSV import finished without errors")
            messages.success(
                self.request,
                _("CSV import finished without errors"),
            )

        return super().form_valid(form)
