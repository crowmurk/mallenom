import calendar
import datetime

from django import template
from django.urls import reverse

from workcal.models import Day


register = template.Library()


@register.tag()
def work_calendar(parser, token):
    try:
        tag_name, year = token.split_contents()
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires a single argument (year)" % token.contents.split()[0]
        )
    return WorkCalendarNode(year)


class WorkCalendarNode(template.Node):
    def __init__(self, year):
        self.year = template.Variable(year)

    def render(self, context):
        year = self.year.resolve(context)
        locale = context.get('request').LANGUAGE_CODE
        return WorkCalendar(locale=locale).formatyear(theyear=year)


class WorkCalendar(calendar.LocaleHTMLCalendar):
    def __init__(self, firstweekday=0, locale=None):
        locales = {
            'en': 'en_US.UTF-8',
            'ru': 'ru_RU.UTF-8',
        }

        month_name_ru = [
            '', 'Январь', 'Февраль', 'Март',
            'Апрель', 'Май', 'Июнь', 'Июль', 'Август',
            'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь',
        ]

        month_name_en = [
            '', 'January', 'February', 'March', 'April',
            'May', 'June', 'July', 'August', 'September',
            'October', 'November', 'December',
        ]

        if locale in locales:
            locale = locales[locale]
            if locale == locales['ru']:
                calendar.month_name = month_name_ru
            if locale == locales['en']:
                calendar.month_name = month_name_en

        self.unusual_days = {
            day.date: {
                'css_class': day.day_type.css_class,
                'url': day.get_absolute_url(),
            } for day in Day.objects.all()
        }
        self.cssclass_year_head = 'year-head'

        self.day_create_url = reverse('workcal:day:create')

        super(WorkCalendar, self).__init__(firstweekday, locale)

    def formatmonth(self, theyear, themonth, withyear=True):
        self.year, self.month = theyear, themonth
        return super(WorkCalendar, self).formatmonth(
            theyear,
            themonth,
            withyear=withyear,
        )

    def formatday(self, day, weekday):
        """ Return a day as a table cell.
        """
        if day == 0:
            return '<td class="%s">&nbsp;</td>' % self.cssclass_noday
        else:
            date = datetime.date(self.year, self.month, day)
            unusual_day = self.unusual_days.get(date)

            if unusual_day:
                return '<td class="{csscls}"><a class="{acls}" href="{url}">{day}</a></td>'.format(
                    csscls=self.cssclasses[weekday],
                    acls=unusual_day['css_class'],
                    url=unusual_day['url'],
                    day=day,
                )
            else:
                return '<td class="{csscls}"><a href="{url}?date={date}">{day}</a></td>'.format(
                    csscls=self.cssclasses[weekday],
                    url=self.day_create_url,
                    date=date,
                    day=day,
                )
