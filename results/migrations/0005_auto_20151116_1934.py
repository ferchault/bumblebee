# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0004_auto_20151109_1827'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bucket',
            name='comment',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='token',
            field=models.CharField(max_length=50, blank=True),
        ),
        migrations.AlterField(
            model_name='bucket',
            name='updated',
            field=models.DateTimeField(blank=True),
        ),
        migrations.AlterField(
            model_name='mdrun',
            name='type',
            field=models.CharField(max_length=20, blank=True),
        ),
        migrations.AlterField(
            model_name='mdrunsettings',
            name='multiplicity',
            field=models.IntegerField(blank=True),
        ),
        migrations.AlterField(
            model_name='mdrunsettings',
            name='pressure',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='mdrunsettings',
            name='temperature',
            field=models.FloatField(blank=True),
        ),
        migrations.AlterField(
            model_name='mdrunsettings',
            name='timestep',
            field=models.FloatField(blank=True),
        ),
    ]
