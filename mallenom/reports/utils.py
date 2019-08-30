import datetime
from copy import deepcopy

from django.db.models import F, Value as V, Sum, PositiveSmallIntegerField
from django.db.models.expressions import Subquery, OuterRef
from django.db.models.functions import Concat, Coalesce

from workcal.models import Day
from schedule.models import Assignment, ProjectAssignment, Absence


class DataBuilder:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    @staticmethod
    def _get_assignment_queryset(start, end, *fields):
        """Формирует queryset к Assignment
        """
        project_hours = Subquery(
            ProjectAssignment.objects.filter(
                project=OuterRef('projectassignments__project'),
                assignment__employment=OuterRef('employment'),
                assignment__start__gte=start,
                assignment__end__lte=end,
            ).values('project').order_by('project').annotate(
                sum=Coalesce(Sum('hours'), 0)
            ).values('sum'),
            output_field=PositiveSmallIntegerField(),
        )

        employment_hours = Subquery(
            ProjectAssignment.objects.filter(
                assignment__employment=OuterRef('employment'),
                assignment__start__gte=start,
                assignment__end__lte=end,
            ).values('assignment__employment').order_by('assignment__employment').annotate(
                sum=Coalesce(Sum('hours'), 0)
            ).values('sum'),
            output_field=PositiveSmallIntegerField(),
        )

        queryset = Assignment.objects.filter(
            projects__isnull=False,
            start__gte=start,
            end__lte=end,
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

    @staticmethod
    def _get_absence_queryset(start, end, *fields):
        """Формирует queryset к Absence
        """
        queryset = Absence.objects.filter(
            end__gte=start,
            start__lte=end
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

    @staticmethod
    def _update_data(data, ajoined, search_fields, update_fields, factor):
        data = deepcopy(data)
        ajoined = deepcopy(ajoined)

        for item in ajoined:
            for field in update_fields:
                item[field] *= factor

            index = next((
                index for index, value in enumerate(data)
                if all([value[field] == item[field] for field in search_fields])
            ), None)

            if index is not None:
                for field in update_fields:
                    data[index][field] += item[field]
            else:
                data.append(item)

        return data

    def _get_assignment_data(self, fields):
        search_fields = tuple(filter(
            lambda i: i in fields,
            ('number', 'project'),
        ))
        update_fields = tuple(filter(
            lambda i: i in fields,
            ('project_hours', 'employment_hours'),
        ))

        data = list(self._get_assignment_queryset(self.start, self.end, *fields))

        if self.start.weekday():
            week_start = self.start - datetime.timedelta(days=self.start.weekday())
            week_end = self.start + datetime.timedelta(days=6 - self.start.weekday())
            week = list(self._get_assignment_queryset(week_start, week_end, *fields))

            total_work_hours = Day.objects.get_work_hours_count(week_start, week_end)
            part_work_hours = Day.objects.get_work_hours_count(self.start, week_end)
            factor = part_work_hours / total_work_hours

            data = self._update_data(
                data, week,
                search_fields, update_fields,
                factor,
            )

        if self.end.weekday() < 6:
            week_start = self.end - datetime.timedelta(days=self.end.weekday())
            week_end = self.end + datetime.timedelta(days=6 - self.end.weekday())
            week = list(self._get_assignment_queryset(week_start, week_end, *fields))

            total_work_hours = Day.objects.get_work_hours_count(week_start, week_end)
            part_work_hours = Day.objects.get_work_hours_count(week_start, self.end)
            factor = part_work_hours / total_work_hours

            data = self._update_data(
                data, week,
                search_fields, update_fields,
                factor,
            )

        return data

    def _get_absence_data(self, fields):
        queryset_fields = list(fields)
        queryset_fields.extend(['start', 'end'])
        data = list(self._get_absence_queryset(self.start, self.end, *queryset_fields))

        for item in data:
            if self.start <= item['start'] and self.end >= item['end']:
                continue

            absence_work_hours = Day.objects.get_work_hours_count(item['start'], item['end'])

            if item['start'] < self.start and item['end'] > self.end:
                intersection_work_hours = Day.objects.get_work_hours_count(self.start, self.end)
            elif item['start'] >= self.start and item['end'] > self.end:
                intersection_work_hours = Day.objects.get_work_hours_count(item['start'], self.end)
            elif item['start'] < self.start and item['end'] <= self.end:
                intersection_work_hours = Day.objects.get_work_hours_count(self.start, item['end'])

            item['absence_hours'] *= (intersection_work_hours / absence_work_hours)

        data = self._update_data([], data, ('number', ), ('absence_hours', ), 1)

        data = [{key: item[key] for key in fields} for item in data]

        return data

    def assignment_report(self):
        """Формирует данные для размещения в отчете
        """
        fields = (
            'employee', 'number', 'department',
            'position', 'project', 'project_hours'
        )
        data = self._get_assignment_data(fields)
        return sorted([tuple(item[key] for key in fields) for item in data])

    def assignment_matrix_report(self, absence_name):
        """Формирует данные для размещения в отчете
        """
        fields = (
            'employee', 'number', 'project', 'project_hours',
        )
        data = self._get_assignment_data(fields)
        data = [[item[key] for key in fields] for item in data]

        absence_fields = ('employee', 'number', 'absence_hours')
        absence_data = self._get_absence_data(absence_fields)
        absence_data = [
            [item[key] for key in absence_fields]
            for item in absence_data
        ]
        for item in absence_data:
            item.insert(2, absence_name)

        data.extend(absence_data)
        return data

    def assignment_hours_check(self):
        """Формирует данные для размещения в отчете
        """
        work_hours_total = Day.objects.get_work_hours_count(self.start, self.end)

        fields = [
            'employee', 'number', 'department', 'position',
            'staff_units', 'employment_hours',
        ]
        data = self._get_assignment_data(fields)

        absence_fields = [
            'employee', 'number', 'department', 'position',
            'staff_units', 'absence_hours',
        ]
        absence_data = self._get_absence_data(absence_fields)

        for item in absence_data:
            index = next((
                index for index, value in enumerate(data)
                if item['number'] == value['number']
            ), None)

            if index is not None:
                data[index]['absence_hours'] = item['absence_hours']
            else:
                data.append(item)

        for item in data:
            item['absence_hours'] = item.get('absence_hours', 0)
            item['employment_hours'] = item.get('employment_hours', 0)
            item['hours_assigned_total'] = item['absence_hours'] + item['employment_hours']
            item['work_hours_total'] = work_hours_total * item['staff_units']

        fields.append('absence_hours')
        fields.append('hours_assigned_total')
        fields.append('work_hours_total')

        return sorted([[item[key] for key in fields] for item in data])
