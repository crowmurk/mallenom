# Generated by Django 2.2.7 on 2020-01-28 16:40

from django.db import migrations, models
import django.db.models.expressions
import schedule.validators


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0007_change_absences_from_employee_to_employment'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='assignment',
            name='correct_assignment_week_range',
        ),
        migrations.AlterField(
            model_name='assignment',
            name='end',
            field=models.DateField(validators=[schedule.validators.validate_assignment_end], verbose_name='End'),
        ),
        migrations.AlterField(
            model_name='assignment',
            name='start',
            field=models.DateField(validators=[schedule.validators.validate_assignment_start], verbose_name='Start'),
        ),
        migrations.AddConstraint(
            model_name='assignment',
            constraint=models.CheckConstraint(check=models.Q(start__lte=django.db.models.expressions.F('end')), name='correct_assignment_range'),
        ),
    ]