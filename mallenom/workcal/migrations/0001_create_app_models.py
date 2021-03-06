# Generated by Django 2.2.3 on 2019-08-08 08:25

import core.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import re


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DayType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True, verbose_name='Name')),
                ('hours', models.PositiveSmallIntegerField(validators=[django.core.validators.MaxValueValidator(24)], verbose_name='Hours')),
                ('csv_mark', models.CharField(blank=True, max_length=1, unique=True, verbose_name='Mark in CSV file')),
                ('css_class', models.CharField(blank=True, max_length=128, validators=[django.core.validators.RegexValidator(regex='^-?[_a-zA-Z]+[_a-zA-Z0-9-]*$')], verbose_name='CSS class')),
                ('slug', models.SlugField(allow_unicode=True, editable=False, help_text='A label for URL config.', max_length=64, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-\\w]+\\Z'), "Enter a valid 'slug' consisting of Unicode letters, numbers, underscores, or hyphens.", 'invalid'), core.validators.validate_slug])),
            ],
            options={
                'verbose_name': 'Day type',
                'verbose_name_plural': 'Day types',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='Day',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(unique=True, verbose_name='Day')),
                ('slug', models.SlugField(allow_unicode=True, editable=False, help_text='A label for URL config.', max_length=32, unique=True, validators=[django.core.validators.RegexValidator(re.compile('^[-\\w]+\\Z'), "Enter a valid 'slug' consisting of Unicode letters, numbers, underscores, or hyphens.", 'invalid'), core.validators.validate_slug])),
                ('day_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='days', to='workcal.DayType', verbose_name='Day type')),
            ],
            options={
                'verbose_name': 'Day',
                'verbose_name_plural': 'Days',
                'ordering': ['-date'],
            },
        ),
    ]
