# Generated by Django 2.2.3 on 2019-07-30 18:46

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('staffing', '0002_change_staffing_verbose_names'),
    ]

    operations = [
        migrations.AlterField(
            model_name='staffing',
            name='count',
            field=models.FloatField(default=1, validators=[django.core.validators.MinValueValidator(0)], verbose_name='Staff units count'),
        ),
    ]