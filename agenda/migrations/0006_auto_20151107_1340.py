# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import agenda.models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0005_auto_20151106_0753'),
    ]

    operations = [
        migrations.AddField(
            model_name='todostatus',
            name='needshuman',
            field=models.BooleanField(default=False, help_text=b'Whether human interaction is required at this stage.'),
        ),
        migrations.AddField(
            model_name='todostatus',
            name='waitingexternal',
            field=models.BooleanField(default=False, help_text=b'Whether propagation from this stage requires external actions.'),
        ),
        migrations.AlterField(
            model_name='project',
            name='parent',
            field=models.ForeignKey(default=None, validators=[agenda.models.LimitSelfReferenceDepth(1, b'Project')], to='agenda.Project', null=True),
        ),
        migrations.AlterField(
            model_name='todostatus',
            name='completed',
            field=models.BooleanField(default=False, help_text=b'Whether elements past this stage are not relevant to planning.'),
        ),
    ]
