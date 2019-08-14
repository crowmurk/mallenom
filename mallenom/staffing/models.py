from django.db import models
from django.db.models.expressions import Subquery, OuterRef
from django.db.models.functions import Coalesce
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_unicode_slug, MinValueValidator

from core.validators import validate_slug
from core.utils import get_unique_slug

# Create your models here.

class DepartmentManager(models.Manager):
    def get_queryset(self):
        staff_units_held = Subquery(
            Staffing.objects.filter(
                department=OuterRef('pk')
            ).values('department').order_by('department').annotate(
                sum=Coalesce(models.Sum('employments__count'), 0)
            ).values('sum')
        )

        return super().get_queryset().annotate(
            positions_count=models.Count('positions'),
            staff_units_count=models.functions.Coalesce(
                models.Sum('staffing__count'), 0
            ),
            staff_units_held=staff_units_held,
        )


class Department(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Name'),
    )
    slug = models.SlugField(
        max_length=128,
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
        'Position',
        related_name='departments',
        through='Staffing',
        through_fields=('department', 'position'),
        verbose_name=_('Positions'),
    )

    objects = DepartmentManager()

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')
        ordering = ['name', ]

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, 'slug', 'name', unique=True)
        super(Department, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'staffing:department:detail',
            kwargs={'slug': self.slug},
        )

    def get_update_url(self):
        return reverse(
            'staffing:department:update',
            kwargs={'slug': self.slug},
        )

    def get_delete_url(self):
        return reverse(
            'staffing:department:delete',
            kwargs={'slug': self.slug},
        )


class PositionManager(models.Manager):
    def get_queryset(self):
        staff_units_held = Subquery(
            Staffing.objects.filter(
                position=OuterRef('pk')
            ).values('position').order_by('position').annotate(
                sum=Coalesce(models.Sum('employments__count'), 0)
            ).values('sum')
        )

        return super().get_queryset().annotate(
            departments_count=models.Count('departments'),
            staff_units_count=models.functions.Coalesce(
                models.Sum('staffing__count'), 0
            ),
            staff_units_held=staff_units_held,
        )


class Position(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Name'),
    )
    slug = models.SlugField(
        max_length=128,
        unique=True,
        editable=False,
        allow_unicode=True,
        validators=[
            validate_unicode_slug,
            validate_slug,
        ],
        help_text=_('A label for URL config.'),
    )

    objects = PositionManager()

    class Meta:
        verbose_name = _('Position')
        verbose_name_plural = _('Positions')
        ordering = ['name', ]

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, 'slug', 'name', unique=True)
        super(Position, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'staffing:position:detail',
            kwargs={'slug': self.slug},
        )

    def get_update_url(self):
        return reverse(
            'staffing:position:update',
            kwargs={'slug': self.slug},
        )

    def get_delete_url(self):
        return reverse(
            'staffing:position:delete',
            kwargs={'slug': self.slug},
        )


class StaffingManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().select_related(
            'department', 'position',
        ).annotate(
            staff_units_held=models.functions.Coalesce(
                models.Sum('employments__count'), 0
            )
        )


class Staffing(models.Model):
    department = models.ForeignKey(
        Department,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='staffing',
        verbose_name=_('Department'),
    )
    position = models.ForeignKey(
        Position,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='staffing',
        verbose_name=_('Position'),
    )
    count = models.FloatField(
        null=False,
        blank=False,
        default=1,
        validators=[
            MinValueValidator(0),
        ],
        verbose_name=_('Staff units count'),
    )

    objects = StaffingManager()

    class Meta:
        verbose_name = _('Staff unit')
        verbose_name_plural = _('Staff units')
        unique_together = (('department', 'position'),)
        ordering = ['position__name', 'department__name']

    def __str__(self):
        return _("{position} ({department_verbose}: {department})").format(
            position=self.position,
            department_verbose=self.department._meta.verbose_name,
            department=self.department,
        )

    def get_absolute_url(self):
        return reverse(
            'staffing:staffing:detail',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'staffing:staffing:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'staffing:staffing:delete',
            kwargs={'pk': self.pk},
        )
