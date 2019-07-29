# Generated by Django 2.2.3 on 2019-07-28 04:06

import core.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('staffing', '0002_change_staffing_verbose_names'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('last_name', models.CharField(max_length=64, verbose_name='Last name')),
                ('first_name', models.CharField(max_length=64, verbose_name='First name')),
                ('middle_name', models.CharField(blank=True, max_length=64, verbose_name='Middle name')),
                ('slug', models.SlugField(allow_unicode=True, editable=False, help_text='A label for URL config.', max_length=255, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-\\w]+\\Z'), "Enter a valid 'slug' consisting of Unicode letters, numbers, underscores, or hyphens.", 'invalid'), core.validators.validate_slug])),
            ],
            options={
                'verbose_name': 'Employee',
                'verbose_name_plural': 'Employees',
                'ordering': ['last_name', 'first_name', 'middle_name'],
            },
        ),
        migrations.CreateModel(
            name='Employment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(max_length=256, unique=True, verbose_name='Employee ID number')),
                ('count', models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='Staff unit count')),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employments', to='employee.Employee', verbose_name='Employee')),
                ('staffing', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='employments', to='staffing.Staffing', verbose_name='Staff unit')),
            ],
            options={
                'verbose_name': 'Position held',
                'verbose_name_plural': 'Positions held',
                'ordering': ['number'],
            },
        ),
        migrations.AddField(
            model_name='employee',
            name='positions',
            field=models.ManyToManyField(related_name='employees', through='employee.Employment', to='staffing.Staffing', verbose_name='Positions held'),
        ),
    ]