# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0003_auto_20151109_1407'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ScaledCoordinatesWrapped',
            new_name='ScaledCoordinateWrapped',
        ),
        migrations.AddField(
            model_name='mdrunattributes',
            name='mdrun',
            field=models.ForeignKey(default=-1, to='results.MDRun'),
            preserve_default=False,
        ),
    ]
