# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import agenda.models


class Migration(migrations.Migration):

    dependencies = [
        ('agenda', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='parent',
            field=models.ForeignKey(default=None, validators=[agenda.models.LimitSelfReferenceDepth(1, 'Project')], to='agenda.Project', null=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='name',
            field=models.CharField(help_text=b'The name this project is referred to.', max_length=45, verbose_name=b'Project Name'),
        ),
    ]
