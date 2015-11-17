# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import agenda.models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0011_auto_20151117_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='parent',
            field=models.ForeignKey(default=None, validators=[agenda.models.LimitSelfReferenceDepth(1, b'Project')], to='agenda.Project', null=True),
        ),
    ]
