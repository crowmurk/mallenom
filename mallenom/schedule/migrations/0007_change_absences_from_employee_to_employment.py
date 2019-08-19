# Generated by Django 2.2.4 on 2019-08-19 05:23

from django.db import migrations, models
import django.db.models.deletion

def change_employee_to_employment(apps, schema_editor):
    Absence = apps.get_model('schedule', 'Absence')

    for absence in Absence.objects.all():
        absence.employment = absence.employee.employments.first()
        absence.save()

def change_employment_to_employee(apps, schema_editor):
    Absence = apps.get_model('schedule', 'Absence')

    for absence in Absence.objects.all():
        absence.employee = absence.employment.employee
        absence.save()


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_change_count_verbose_name'),
        ('schedule', '0006_change_assignment_employment_verbose_name_again'),
    ]

    operations = [
        migrations.AddField(
            model_name='absence',
            name='employment',
            field=models.ForeignKey(
                default=None,
                null=True,
                blank=True,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='absences',
                to='employee.Employment',
                verbose_name='Position',
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            change_employee_to_employment,
            reverse_code=change_employment_to_employee,
        ),
        migrations.AlterUniqueTogether(
            name='absence',
            unique_together={('employment', 'start', 'end')},
        ),
        migrations.AlterField(
            model_name='absence',
            name='employment',
            field=models.ForeignKey(
                default=None,
                null=False,
                blank=False,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='absences',
                to='employee.Employment',
                verbose_name='Position',
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='absence',
            name='employee',
        ),
    ]
