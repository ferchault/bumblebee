# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0005_auto_20151116_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdrunsettings',
            name='multiplicity',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mdrunsettings',
            name='pressure',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mdrunsettings',
            name='temperature',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mdrunsettings',
            name='timestep',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
