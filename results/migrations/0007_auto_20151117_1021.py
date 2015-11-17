# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0006_auto_20151116_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mdstep',
            name='masked',
            field=models.NullBooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='mdstep',
            name='stepnumber',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='mdstep',
            name='steptime',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcell',
            name='a',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcell',
            name='alpha',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcell',
            name='b',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcell',
            name='beta',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcell',
            name='c',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcell',
            name='gamma',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcontributionsqm',
            name='constraint',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcontributionsqm',
            name='corehamiltonian',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcontributionsqm',
            name='coreselfenergy',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcontributionsqm',
            name='dispersion',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcontributionsqm',
            name='hartree',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcontributionsqm',
            name='hfx',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepcontributionsqm',
            name='xc',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepenergy',
            name='drift',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepenergy',
            name='ekin',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepenergy',
            name='epot',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepenergy',
            name='etot',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepensemble',
            name='conserved',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepensemble',
            name='pressure',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepensemble',
            name='temperature',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepensemble',
            name='volume',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepmetaqm',
            name='iasd',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepmetaqm',
            name='otcycles',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepmetaqm',
            name='s2',
            field=models.FloatField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='stepmetaqm',
            name='scfcycles',
            field=models.FloatField(null=True, blank=True),
        ),
    ]
