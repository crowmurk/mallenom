from django.db.models import F, Value as V, Sum, PositiveSmallIntegerField
from django.db.models.expressions import Subquery, OuterRef
from django.db.models.functions import Concat, Coalesce

from workcal.models import Day
from schedule.models import Assignment, ProjectAssignment, Absence


class DataBuilder:
    def __init__(self, start, end, **kwargs):
        """Формирует данные для размещения в отчетах.

        Args:
            start - начальная дата
            end - конечная дата

        Kwargs:
            precision - точность округления
        """

        # Начальная и конечная даты
        self.start = start
        self.end = end

        # Точность округления
        self.precision = kwargs.get('precision', 2)

    def _get_assignment_queryset(self, *fields):
        """Формирует queryset к Assignment.

        Args:
            *fields - поля запроса

        Returns:
            queryset
        """

        # Сумма часов по проекту для должности (employment)
        project_hours = Subquery(
            ProjectAssignment.objects.filter(
                project=OuterRef('projectassignments__project'),
                assignment__employment=OuterRef('employment'),
                assignment__start__gte=self.start,
                assignment__end__lte=self.end,
            ).values('project').order_by('project').annotate(
                sum=Coalesce(Sum('hours'), 0)
            ).values('sum'),
            output_field=PositiveSmallIntegerField(),
        )

        # Общая сумма часов для должности (employment)
        employment_hours = Subquery(
            ProjectAssignment.objects.filter(
                assignment__employment=OuterRef('employment'),
                assignment__start__gte=self.start,
                assignment__end__lte=self.end,
            ).values('assignment__employment').order_by(
                'assignment__employment'
            ).annotate(
                sum=Coalesce(Sum('hours'), 0)
            ).values('sum'),
            output_field=PositiveSmallIntegerField(),
        )

        # Выбираем записи полностью попадающие в интервал
        queryset = Assignment.objects.filter(
            projects__isnull=False,
            start__gte=self.start,
            end__lte=self.end,
        ).annotate(
            employee=Concat(
                F('employment__employee__last_name'), V(' '),
                F('employment__employee__first_name'), V(' '),
                F('employment__employee__middle_name'),
            ),
            number=F('employment__number'),
            department=F('employment__staffing__department__name'),
            position=F('employment__staffing__position__name'),
            staff_units=F('employment__count'),
            employment_hours=Coalesce(employment_hours, 0),
            project=F('projectassignments__project__name'),
            project_hours=Coalesce(project_hours, 0),
        ).order_by('employee').values(*fields).distinct()

        return queryset

    def _get_absence_queryset(self, *fields):
        """Формирует queryset к Absence.

        Args:
            *fields - поля запроса

        Returns:
            queryset
        """

        # Выбираем записи полностью попадающие в интервал
        queryset = Absence.objects.filter(
            start__gte=self.start,
            end__lte=self.end,
        ).annotate(
            employee=Concat(
                F('employment__employee__last_name'), V(' '),
                F('employment__employee__first_name'), V(' '),
                F('employment__employee__middle_name'),
            ),
            number=F('employment__number'),
            department=F('employment__staffing__department__name'),
            position=F('employment__staffing__position__name'),
            staff_units=F('employment__count'),
            absence_hours=F('hours'),
        ).order_by('employee').values(*fields).distinct()

        return queryset

    def _round_iterable(self, iterable, whole):
        """Округляет значения из списка так, чтобы сумма округленных
        значений списка была равна округленной сумме значений.

        Args:
            iterable - список значений для округления
            whole - округленная сумма значений списка

        Returns:
            список округленных значений
        """

        # Получаем сохраняемые и отбрасываемые при округлении
        # части чисел. Сохраняем позицию элемнтов.
        result = [
            [index, *divmod(item * 10 ** self.precision, 1)]
            for index, item in enumerate(iterable)
        ]

        # Разница между whole и суммой всех округленных элементов
        delta = int(whole * 10 ** self.precision) - sum(
            [int(item[1]) for item in result]
        )

        if delta > len(result):
            raise ValueError("Iterable {iterable} sum must be"
                             " almost equal whole value: {whole}".format(
                                 iterable=iterable,
                                 whole=whole,
                             ))

        # Распределяем delta по списку начиная с элементов
        # с наибольшей отбрасываемой частью
        result = sorted(result, key=lambda i: i[-1], reverse=True)
        for index in range(delta):
            result[index][1] += 1

        # Возвращаем исходный порядок элементов
        result = sorted(result, key=lambda i: i[0])

        # Возвращаем список с округленными значениями
        return [item[1] / 10 ** self.precision for item in result]

    def _get_assignment_data(self, fields):
        """Формирует данные о назначениях.

        Args:
            fields - поля, которые должны присутсвовать в данных

        Returns:
            данные о назначениях
        """

        # Получаем данные из БД
        return list(self._get_assignment_queryset(*fields))

    def _get_absence_data(self, fields):
        """Формирует данные об отсутствиях.

        Args:
            fields - поля, которые должны присутсвовать в данных

        Returns:
            данные об отсутствиях
        """

        # Получаем данные из БД
        return list(self._get_absence_queryset(*fields))

    def assignment_report(self):
        """Формирует данные для размещения в отчете.

        Returns:
            данные для отчета
        """

        # Получаем данные о назначениях
        fields = (
            'employee', 'number', 'department',
            'position', 'project', 'project_hours'
        )
        data = self._get_assignment_data(fields)
        return [[item[key] for key in fields] for item in data]

    def assignment_matrix_report(self, absence_name):
        """Формирует данные для размещения в отчете.

        Args:
            absence_name - наименование для поля 'отсутствие'

        Returns:
            данные для отчета
        """

        # Получаем данные о назначениях
        fields = (
            'employee', 'number', 'project', 'project_hours',
        )
        data = self._get_assignment_data(fields)
        data = [[item[key] for key in fields] for item in data]

        # Получаем данные об отсутствиях
        absence_fields = ('employee', 'number', 'absence_hours')
        absence_data = self._get_absence_data(absence_fields)
        absence_data = [
            [item[key] for key in absence_fields]
            for item in absence_data
        ]

        # Добавляем часы отсутсвия к данным о назначениях
        # как назначение по проекту 'absence_name'
        for item in absence_data:
            item.insert(fields.index('project'), absence_name)
        data.extend(absence_data)

        return data

    def assignment_hours_check(self):
        """Формирует данные для размещения в отчете.

        Returns:
            данные для отчета
        """

        work_hours_total = Day.objects.get_work_hours_count(self.start, self.end)

        # Получаем данные о назначениях
        fields = [
            'employee', 'number', 'department', 'position',
            'staff_units', 'employment_hours',
        ]
        data = self._get_assignment_data(fields)

        # Получаем данные об отсутствиях
        absence_fields = [
            'employee', 'number', 'department', 'position',
            'staff_units', 'absence_hours',
        ]
        absence_data = self._get_absence_data(absence_fields)

        # Обновляем данные о назначениях данными об отсутствиях
        for item in absence_data:
            # Ищем назначение с таким же табельным номером
            index = next((
                index for index, value in enumerate(data)
                if item['number'] == value['number']
            ), None)

            if index is not None:
                # Если назначение найдено, добавляем в него  часы отсутствия
                data[index]['absence_hours'] = item['absence_hours']
            else:
                # Добавляем информацию об отсутствии
                data.append(item)

        for item in data:
            # Эти поля должны присутствовать в каждой записи
            item['absence_hours'] = item.get('absence_hours', 0)
            item['employment_hours'] = item.get('employment_hours', 0)

            # Вычисляем дополнительные поля для отчета
            item['hours_assigned_total'] = item['absence_hours'] + item['employment_hours']
            item['work_hours_total'] = work_hours_total * item['staff_units']
            item['hours_difference'] = abs(
                item['work_hours_total'] - item['hours_assigned_total']
            )

        # Расширяем список полей для отчета
        fields.extend((
            'absence_hours', 'hours_assigned_total',
            'work_hours_total', 'hours_difference',
        ))

        return [[item[key] for key in fields] for item in data]

    def index_of_labor_distribution(self, absence_name):
        """Формирует данные для размещения в отчете.

        Args:
            absence_name - наименование для поля 'отсутствие'

        Returns:
            данные для отчета
        """
        work_hours_total = Day.objects.get_work_hours_count(self.start, self.end)

        # Получаем данные о назначениях
        fields = (
            'employee', 'number', 'staff_units', 'project', 'project_hours',
        )
        data = self._get_assignment_data(fields)

        # Вычисляем долю от общего колличества рабочих часов
        for item in data:
            item['project_hours'] /= work_hours_total

        data = [[item[key] for key in fields] for item in data]

        # Получаем данные об отсутствиях
        absence_fields = ('employee', 'number', 'staff_units', 'absence_hours',)
        absence_data = self._get_absence_data(absence_fields)

        # Вычисляем долю от общего колличества рабочих часов
        for item in absence_data:
            item['absence_hours'] /= work_hours_total

        absence_data = [
            [item[key] for key in absence_fields]
            for item in absence_data
        ]

        # Добавляем часы отсутсвия к данным о назначениях
        # как назначение по проекту 'absence_name'
        for item in absence_data:
            item.insert(fields.index('project'), absence_name)

        data.extend(absence_data)

        # Для каждого табельного номера суммируем часы,
        # округляем и добавляем сумму к данным номера
        for item in data:
            item.append(round(
                sum(
                    [other[4] for other in filter(
                        lambda i: i[1] == item[1],
                        data,
                    )]
                ),
                self.precision,
            ))

        # Для каждого табельного номера и полученной суммы
        # часов необходимо округлить слагаемые
        for employment, employment_hours in set(
                [(item[1], item[5]) for item in data]
        ):
            # Получаем назначеные часы для табельного номера и позицию в данных
            items = [
                (index, item[4])
                for index, item in enumerate(data)
                if item[1] == employment
            ]

            # Округляем часы
            indexes, hours = zip(*items)
            hours = self._round_iterable(hours, employment_hours)

            # Заменяем часы в данных округленными значениями
            for index, hours in zip(indexes, hours):
                data[index][4] = hours

        return data

    def index_of_labor_distribution_per_project(self):
        """Формирует данные для размещения в отчете.

        Returns:
            данные для отчета
        """

        # Получаем данные о назначениях
        fields = (
            'employee', 'number', 'project',
            'project_hours'
        )
        data = self._get_assignment_data(fields)

        # Суммируем часы назначений по каждому табельному
        # номеру сохраняем в данные
        for item in data:
            item['employment_hours'] = sum(
                [other['project_hours'] for other in filter(
                    lambda i: i['number'] == item['number'],
                    data,
                )]
            )

        # Вычисляем долю от общего колличества часов
        for item in data:
            item['project_hours'] /= item['employment_hours']

        # Для каждого табельного номера необходимо округлить полученые доли
        for employment in set([item['number'] for item in data]):
            # Получаем доли назначений для табельного номера и позицию в данных
            items = [
                (index, item['project_hours'])
                for index, item in enumerate(data)
                if item['number'] == employment
            ]

            # Округляем доли
            indexes, hours = zip(*items)
            hours = self._round_iterable(hours, 1)

            # Заменяем доли в данных округленными значениями
            for index, hours in zip(indexes, hours):
                data[index]['project_hours'] = hours

        return [[item[key] for key in fields] for item in data]
