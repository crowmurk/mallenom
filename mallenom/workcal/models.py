from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    validate_unicode_slug,
    MaxValueValidator,
    RegexValidator,
)

from core.validators import validate_slug
from core.utils import get_unique_slug

# Create your models here.

class DayTypeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().prefetch_related(
            'days',
        ).annotate(days_count=models.Count('days'))


class DayType(models.Model):
    name = models.CharField(
        max_length=64,
        unique=True,
        verbose_name=_('Name'),
    )
    hours = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[
            MaxValueValidator(24),
        ],
        verbose_name=_('Hours'),
    )
    csv_mark = models.CharField(
        max_length=1,
        unique=True,
        null=False,
        blank=True,
        verbose_name=_('Mark in CSV file'),
    )
    css_class = models.CharField(
        max_length=128,
        unique=False,
        null=False,
        blank=True,
        validators=[
            RegexValidator(
                regex='^-?[_a-zA-Z]+[_a-zA-Z0-9-]*$',
            ),
        ],
        verbose_name=_('CSS class'),
    )
    slug = models.SlugField(
        max_length=64,
        unique=True,
        editable=False,
        allow_unicode=True,
        validators=[
            validate_unicode_slug,
            validate_slug,
        ],
        help_text=_('A label for URL config.'),
    )

    objects = DayTypeManager()

    class Meta:
        verbose_name = _('Day type')
        verbose_name_plural = _('Day types')
        ordering = ['name', ]

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, 'slug', 'name', unique=True)
        super(DayType, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'workcal:daytype:detail',
            kwargs={'slug': self.slug},
        )

    def get_update_url(self):
        return reverse(
            'workcal:daytype:update',
            kwargs={'slug': self.slug},
        )

    def get_delete_url(self):
        return reverse(
            'workcal:daytype:delete',
            kwargs={'slug': self.slug},
        )


class DayManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'day_type',
        )

    def get_days(self, start, end):
        if start > end:
            start, end = end, start

        return self.get_queryset().filter(
            date__gte=start,
            date__lte=end,
        )

    def get_rest_days(self, start, end):
        return self.get_days(start, end).filter(
            day_type__hours=0,
        )

    def get_uncommon_days(self, start, end):
        return self.get_days(start, end).filter(
            day_type__hours__gt=0,
        )

    def get_work_days_count(self, start, end):
        days_total = abs(end - start).days + 1
        return days_total - self.get_rest_days(start, end).count()

    def get_work_hours_count(self, start, end,
                             day_hours=settings.WORK_DAY_HOURS):
        work_days = self.get_work_days_count(start, end)
        uncommon_days = self.get_uncommon_days(start, end).aggregate(
            count=models.Count('id'),
            hours=models.functions.Coalesce(
                models.Sum('day_type__hours'), 0
            ),
        )
        return (work_days - uncommon_days['count']) * day_hours + uncommon_days['hours']


class Day(models.Model):
    date = models.DateField(
        unique=True,
        verbose_name=_('Day'),
    )
    day_type = models.ForeignKey(
        DayType,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='days',
        verbose_name=_('Day type'),
    )
    slug = models.SlugField(
        max_length=32,
        unique=True,
        editable=False,
        allow_unicode=True,
        validators=[
            validate_unicode_slug,
            validate_slug,
        ],
        help_text=_('A label for URL config.'),
    )

    objects = DayManager()

    class Meta:
        verbose_name = _('Day')
        verbose_name_plural = _('Days')
        ordering = ['-date', ]

    def __str__(self):
        return "{date}: {day_type}".format(
            date=self.date,
            day_type=self.day_type,
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, 'slug', 'date', unique=True)
        super(Day, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'workcal:day:detail',
            kwargs={'slug': self.slug},
        )

    def get_update_url(self):
        return reverse(
            'workcal:day:update',
            kwargs={'slug': self.slug},
        )

    def get_delete_url(self):
        return reverse(
            'workcal:day:delete',
            kwargs={'slug': self.slug},
        )
