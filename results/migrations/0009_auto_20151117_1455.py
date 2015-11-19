# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0008_auto_20151117_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coordinate',
            name='x',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='coordinate',
            name='y',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='coordinate',
            name='z',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mullikencharge',
            name='alpha',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mullikencharge',
            name='beta',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mullikencharge',
            name='charge',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mullikencharge',
            name='spin',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
