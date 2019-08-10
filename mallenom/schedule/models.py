import datetime

from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import validate_unicode_slug, MaxValueValidator

from core.validators import (
    validate_slug,
    validate_monday,
    validate_sunday,
    validate_positive,
)
from core.utils import get_unique_slug

from employee.models import Employee

# Create your models here.

class ProjectManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            hours=models.functions.Coalesce(
                models.Sum('projectassignments__hours'), 0
            ),
            assignments_count=models.Count('projectassignments'),
        )

class Project(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        verbose_name=_('Name'),
    )
    status = models.BooleanField(
        null=False,
        blank=False,
        default=True,
        verbose_name=_('Status'),
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

    objects = ProjectManager()

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['name', ]

    def __str__(self):
        return "{name}".format(
            name=self.name,
        )

    def save(self, *args, **kwargs):
        self.slug = get_unique_slug(self, 'slug', 'name', unique=True)
        super(Project, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse(
            'schedule:project:detail',
            kwargs={'slug': self.slug},
        )

    def get_update_url(self):
        return reverse(
            'schedule:project:update',
            kwargs={'slug': self.slug},
        )

    def get_delete_url(self):
        return reverse(
            'schedule:project:delete',
            kwargs={'slug': self.slug},
        )


class AssignmentManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().annotate(
            hours=models.functions.Coalesce(
                models.Sum('projectassignments__hours'), 0
            ),
        )


class Assignment(models.Model):
    employee = models.ForeignKey(
        Employee,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='assignments',
        verbose_name=_('Employee'),
    )
    start = models.DateField(
        null=False,
        blank=False,
        validators=[
            validate_monday,
        ],
        verbose_name=_('Start'),
    )
    end = models.DateField(
        null=False,
        blank=False,
        validators=[
            validate_sunday,
        ],
        verbose_name=_('End'),
    )
    projects = models.ManyToManyField(
        'Project',
        related_name='assignments',
        through='ProjectAssignment',
        through_fields=('assignment', 'project'),
        verbose_name=_('Projects'),
    )

    objects = AssignmentManager()

    class Meta:
        verbose_name = _("Employee's assignments")
        verbose_name_plural = _("Employees' assignments")
        unique_together = (('employee', 'start', 'end',),)
        ordering = ['-start', ]
        constraints = [
            models.CheckConstraint(
                check=models.Q(
                    start__exact=models.F('end') - datetime.timedelta(days=6)
                ),
                name='correct_assignment_week_range',
            ),
        ]

    def __str__(self):
        return _("{start}-{end}: {employee}").format(
            start=self.start,
            end=self.end,
            employee=self.employee,
        )

    def get_absolute_url(self):
        return reverse(
            'schedule:assignment:detail',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'schedule:assignment:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'schedule:assignment:delete',
            kwargs={'pk': self.pk},
        )


class ProjectAssignment(models.Model):
    project = models.ForeignKey(
        Project,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='projectassignments',
        verbose_name=_('Project'),
    )
    assignment = models.ForeignKey(
        Assignment,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='projectassignments',
        verbose_name=_('Assignment'),
    )
    hours = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[
            validate_positive,
            MaxValueValidator(168),
        ],
        verbose_name=_('Hours'),
    )

    class Meta:
        verbose_name = _("Project's assigment")
        verbose_name_plural = _("Projects' assigments")
        unique_together = (('assignment', 'project'),)
        ordering = ['-assignment__start', ]

    def __str__(self):
        return _("Assignment: {assignment} Project: {project}"
                 " Hours: {hours}").format(
                     assignment=self.assignment.pk,
                     project=self.project.name,
                     hours=self.hours,
        )

    def get_absolute_url(self):
        return reverse(
            'schedule:projectassignment:detail',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'schedule:projectassignment:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'schedule:projectassignment:delete',
            kwargs={'pk': self.pk},
        )


class Absence(models.Model):
    employee = models.ForeignKey(
        Employee,
        null=False,
        blank=False,
        on_delete=models.PROTECT,
        related_name='absences',
        verbose_name=_('Employee'),
    )
    start = models.DateField(
        null=False,
        blank=False,
        verbose_name=_('Start'),
    )
    end = models.DateField(
        null=False,
        blank=False,
        verbose_name=_('End'),
    )
    hours = models.PositiveSmallIntegerField(
        null=False,
        blank=False,
        validators=[
            validate_positive,
        ],
        verbose_name=_('Hours'),
    )
    reason = models.TextField(
        null=False,
        blank=True,
        verbose_name=_('Reason'),
        help_text=_('Reason for employee absence'),
    )

    class Meta:
        verbose_name = _("Employee's absence")
        verbose_name_plural = _("Employees' absences")
        unique_together = (('employee', 'start', 'end'),)
        ordering = ['-start']
        constraints = [
            models.CheckConstraint(
                check=models.Q(start__lte=models.F('end')),
                name='correct_employee_absence_range',
            ),
        ]

    def __str__(self):
        return _("{start}-{end}: {employee} {hours}").format(
            start=self.start,
            end=self.end,
            employee=self.employee,
            hours=self.hours,
        )

    def get_absolute_url(self):
        return reverse(
            'schedule:absence:detail',
            kwargs={'pk': self.pk},
        )

    def get_update_url(self):
        return reverse(
            'schedule:absence:update',
            kwargs={'pk': self.pk},
        )

    def get_delete_url(self):
        return reverse(
            'schedule:absence:delete',
            kwargs={'pk': self.pk},
        )
