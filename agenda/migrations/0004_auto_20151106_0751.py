# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import agenda.models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0003_auto_20151106_0730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='active',
            field=models.BooleanField(verbose_name=b'Active?'),
        ),
        migrations.AlterField(
            model_name='project',
            name='parent',
            field=models.ForeignKey(default=None, validators=[agenda.models.LimitSelfReferenceDepth(1, b'Project')], to='agenda.Project', null=True),
        ),
        migrations.AlterField(
            model_name='todoentry',
            name='duedate',
            field=models.DateField(null=True),
        ),
    ]
