from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import (
    validate_unicode_slug,
    MinValueValidator,
    MaxValueValidator,
)

from core.validators import validate_slug
from core.utils import get_unique_slug

from staffing.models import Staffing

# Create your models here.

class EmployeeManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            full_name=models.functions.LTrim(
                models.functions.Concat(
                    'last_name', models.Value(' '),
                    'first_name', models.Value(' '),
                    'middle_name',
                    output_field=models.CharField(),
                )
            )
        ).annotate(
            departments=models.Count(
                'employments__staffing__department',
                distinct=True,
            )
        ).annotate(
            positions_held=models.Count(
                'employments',
                distinct=True,
            )
        ).annotate(
            staff_units_count=models.functions.Coalesce(
                models.Sum('employments__count'), 0
            ),
        )


class Employee(models.Model):
    last_name = models.CharField(
        max_length=64,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('Last name'),
    )
    first_name = models.CharField(
        max_length=64,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('First name'),
    )
    middle_name = models.CharField(
        max_length=64,
        unique=False,
        null=False,
        blank=True,
        verbose_name=_('Middle name'),
    )
    slug = models.SlugField(
        max_length=255,
        unique=True,
        editable=False,
        allow_unicode=True,
        validators=[
            validate_unicode_slug,
            validate_slug,
        ],
        help_text=_('A label for URL config.'),
    )
    positions = models.ManyToManyField(
        'staffing.Staffing',
        related_name='employees',
        through='Employment',
        through_fields=('employee', 'staffing'),
        verbose_name=_('Positions held'),
    )

    objects = EmployeeManager()

    class Meta:
        verbose_name = _('Employee')
        verbose_name_plural = _('Employees')
        ordering = ['last_name', 'first_name', 'middle_name']

    def __str__(self):
        return ' '.join((
            self.last_name,
            self.first_name,
            self.middle_name,
        ))

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(
            self,
            'slug',
            *('last_name', 'first_name', 'middle_name'),
            unique=True,
        )
        super(Employee, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'employee:employee:detail',
            kwargs={'slug': self.slug},
        )

    def get_update_url(self):
        return reverse(
            'employee:employee:update',
            kwargs={'slug': self.slug},
        )

    def get_delete_url(self):
        return reverse(
            'employee:employee:delete',
            kwargs={'slug': self.slug},
        )


class Employment(models.Model):
    number = models.CharField(
        max_length=256,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('Employee ID number'),
    )
    employee = models.ForeignKey(
        Employee,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='employments',
        verbose_name=_('Employee'),
    )
    staffing = models.ForeignKey(
        Staffing,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='employments',
        verbose_name=_('Staff unit'),
    )
    count = models.FloatField(
        null=False,
        blank=False,
        default=1,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(1),
        ],
        verbose_name=_('Staff units count'),
    )

    class Meta:
        verbose_name = _('Position held')
        verbose_name_plural = _('Positions held')
        ordering = ['number', ]

    def __str__(self):
        return "{number}: {employee}".format(
            number=self.number,
            employee=self.employee,
        )

    def get_absolute_url(self):
        return reverse(
            'employee:employment:detail',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'employee:employment:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'employee:employment:delete',
            kwargs={'pk': self.pk},
        )
