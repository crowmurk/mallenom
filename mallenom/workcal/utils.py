import datetime
import csv
import urllib.request
from copy import deepcopy

from django.utils.translation import ugettext_lazy as _

from .models import DayType


class WorkCalendarParser:
    """Анализирует набор в csv формате содержащий
    производственный календарь.
    """
    # Поддерживаемые языки
    languages = ('en', 'ru')

    # Конфигурация csv формата
    csv_config = {
        # Разделитель ячеек
        'cellDelimeter': ',',
        # Разделитель объединенных значений
        'valueDelimeter': ',',
        # Символ объединения значений в ячейке
        'quote': '"',
    }

    # Имя столбца c годами
    year = {
        'en': 'Year/Month',
        'ru': 'Год/Месяц',
    }

    # Имена столбцов с месяцами
    months = {
        'en': (
            'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'September',
            'October', 'November', 'December',
        ),

        'ru': (
            'Январь', 'Февраль', 'Март', 'Апрель',
            'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь',
            'Октябрь', 'Ноябрь', 'Декабрь',
        ),

    }

    def __init__(self, data=None, *, language='ru', **kwargs):
        """Анализирует набор в csv формате содержащий
        производственный календарь.

        Args:
            data: набор данных

        Kwargs:
            language: язык csv файла
            ...
        """
        if language in self.languages:
            self.language = language
        else:
            raise ValueError(
                _("Language '{}' does not supported").format(
                    language
                )
            )

        # Обновляем параметры работы из kwargs
        for item in self.csv_config:
            self.csv_config[item] = kwargs.get(
                item,
                self.csv_config[item],
            )

        for attr in ('months', 'year'):
            setattr(self, attr, kwargs.get(
                attr,
                getattr(self, attr)[self.language],
            ))

        # Получаем отметки типов дней из БД
        day_types = list(DayType.objects.values('id', 'csv_mark'))
        if not day_types:
            raise ValueError(_("Day types not specified"))
        self.day_types = {
            day_type['csv_mark']: day_type['id']
            for day_type in day_types
        }

        if data:
            if isinstance(data, str):
                # Передана строка с данными
                self.calendar = self._parser(data)
            elif isinstance(data, dict):
                # Передан календарь
                self.calendar = data
            else:
                self.calendar = {}
        else:
            self.calendar = {}

    @classmethod
    def fromFile(cls, fileName, **kwargs):
        """Загружает набор данных из файла.

        Args:
            fileName: файл с набором данных

        Kwargs:
            ...
        """
        data = ''
        with open(fileName, 'r') as file:
            data = file.read()
        return cls(data=data, **kwargs)

    @classmethod
    def fromURL(cls, url, **kwargs):
        """Загружает набор данных по ссылке.

        Args:
            url: ссылка на файл с набором данных

        Kwargs:
            ...
        """
        data = ''
        with urllib.request.urlopen(url) as file:
            data = file.read().decode('utf-8')
        return cls(data=data, **kwargs)

    def _convertYear(self, year, months):
        """Преобразует данные о днях в структуру вида
        [{'date': dateObject, 'day_type': id},...]

        Args:
            year - текущий год
            months - месяцы и дни в виде:
               {month: [day,...],...}
        """

        result = []

        for month, days in months.items():
            for day in days:
                day_type = None
                try:
                    # Если обычный день, без отметок, получаем дату
                    date = datetime.date(year, month, int(day))
                    # Добавляем запись
                    result.append({'date': date, 'day_type': self.day_types['']})
                except ValueError:
                    # Проходим по известным типам дней
                    for day_type_mark, day_type_id in self.day_types.items():
                        if day_type_mark and day_type_mark in day:
                            # Если присутстует отметка о типе дня
                            try:
                                # Убираем отметку и получаем дату
                                date = datetime.date(
                                    year,
                                    month,
                                    int(day.strip(day_type_mark)),
                                )
                            except ValueError:
                                raise ValueError(
                                    _("Invalid day format: '{}'").format(day)
                                )

                            # Добавляем запись
                            result.append(
                                {'date': date, 'day_type': day_type_id}
                            )
                            day_type = day_type_id
                            break

                    if day_type is None:
                        # Неизвестная отметка
                        raise ValueError(_("Unknown day type: '{}'").format(day))

        return result

    def _parser(self, data):
        """Парсер набора данных в csv формате
        возвращает структуру вида:
        {year: [{date: dateObject, day_type: id},...],...}

        Args:
            data: набор данных в csv формате
        """

        # Преобразуем csv в список из словарей где каждый элемент
        # содержит данные одной строки из файла, а его ключи - поля csv
        try:
            data = csv.DictReader(
                data.splitlines(),
                delimiter=self.csv_config['cellDelimeter'],
                quotechar=self.csv_config['quote'],
            )
        except csv.Error as error:
            raise csv.Error(_("CSV module exception: {error}").format(error))

        # Преобразуем список в словарь требуемого вида
        try:
            data = {
                int(row[self.year]):
                self._convertYear(
                    int(row[self.year]),
                    # {month: [day,...],...}
                    {index + 1: row[month].split(self.csv_config['valueDelimeter'])
                     for index, month in enumerate(self.months)},
                )
                for row in data
            }
        except LookupError as error:
            raise LookupError(_("Invalid CSV format: {}").format(error))

        return data

    def get_days_list(self, year=None):
        """Возвращает список дней в формате
        [{date: dateObject, day_type: id},...]

        Args:
            year: только дни определенного года
        """
        if not year:
            result = [
                deepcopy(data)
                for _, year_data in self.calendar.items()
                for data in year_data
            ]
        else:
            result = deepcopy(self.calendar.get(year, []))

        return result
