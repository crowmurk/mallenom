from django.db import models
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
        return "{name} - {hours_verbose}: {hours}".format(
            name=self.name,
            hours_verbose=self._meta.get_field('hours').verbose_name,
            hours=self.hours,
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
        return "{date}: {hours} ({day_type})".format(
            date=self.date,
            hours=self.day_type.hours,
            day_type=self.day_type.name,
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
