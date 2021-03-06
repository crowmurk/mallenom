# Generated by Django 2.2.4 on 2019-08-10 13:29

from django.db import migrations, models
import django.db.models.deletion


def change_employee_to_employment(apps, schema_editor):
    Assignment = apps.get_model('schedule', 'Assignment')

    for assignment in Assignment.objects.all():
        assignment.employment = assignment.employee.employments.first()
        assignment.save()

def change_employment_to_employee(apps, schema_editor):
    Assignment = apps.get_model('schedule', 'Assignment')

    for assignment in Assignment.objects.all():
        assignment.employee = assignment.employment.employee
        assignment.save()


class Migration(migrations.Migration):

    dependencies = [
        ('employee', '0002_change_count_verbose_name'),
        ('schedule', '0003_change_projectassignment_ordering'),
    ]

    operations = [
        migrations.AddField(
            model_name='assignment',
            name='employment',
            field=models.ForeignKey(
                null=True,
                blank=True,
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='assignments',
                to='employee.Employment',
                verbose_name='Employee'
            ),
            preserve_default=False,
        ),
        migrations.RunPython(
            change_employee_to_employment,
            reverse_code=change_employment_to_employee,
        ),
        migrations.AlterUniqueTogether(
            name='assignment',
            unique_together={('employment', 'start', 'end')},
        ),
        migrations.AlterField(
            model_name='assignment',
            name='employment',
            field=models.ForeignKey(
                null=False,
                blank=False,
                default=None,
                on_delete=django.db.models.deletion.PROTECT,
                related_name='assignments',
                to='employee.Employment',
                verbose_name='Employee'
            ),
            preserve_default=False,
        ),
        migrations.RemoveField(
            model_name='assignment',
            name='employee',
        ),
    ]
