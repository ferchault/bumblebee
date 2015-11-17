# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0007_auto_20151117_1021'),
    ]

    operations = [
        migrations.AddField(
            model_name='atom',
            name='number',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='atom',
            name='element',
            field=models.CharField(max_length=3, null=True, blank=True),
        ),
    ]
