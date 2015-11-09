# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import bumblebee.models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0002_auto_20151105_0838'),
    ]

    operations = [
        migrations.CreateModel(
            name='Atom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('element', models.CharField(max_length=3)),
                ('kind', models.CharField(max_length=10)),
                ('system', models.ForeignKey(to='results.System')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='Coordinate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('atom', models.ForeignKey(to='results.Atom')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='CoordinateWrapped',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('coordinate', models.ForeignKey(to='results.Coordinate')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='HirshfeldCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge', models.FloatField()),
                ('alpha', models.FloatField()),
                ('beta', models.FloatField()),
                ('spin', models.FloatField()),
                ('reference', models.FloatField()),
                ('atom', models.ForeignKey(to='results.Atom')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='MDRun',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('part', models.IntegerField()),
                ('type', models.CharField(max_length=20)),
                ('series', models.ForeignKey(to='results.Series')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='MDRunAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=45)),
                ('value', models.CharField(max_length=200)),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='MDRunSettings',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temperature', models.FloatField()),
                ('pressure', models.FloatField()),
                ('multiplicity', models.IntegerField()),
                ('timestep', models.FloatField()),
                ('mdrun', models.ForeignKey(to='results.MDRun')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='MDStep',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('stepnumber', models.IntegerField()),
                ('steptime', models.FloatField()),
                ('masked', models.BooleanField()),
                ('mdrun', models.ForeignKey(to='results.MDRun')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='MullikenCharge',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('charge', models.FloatField()),
                ('alpha', models.FloatField()),
                ('beta', models.FloatField()),
                ('spin', models.FloatField()),
                ('atom', models.ForeignKey(to='results.Atom')),
                ('mdstep', models.ForeignKey(to='results.MDStep')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='ScaledCoordinate',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('atom', models.ForeignKey(to='results.Atom')),
                ('mdstep', models.ForeignKey(to='results.MDStep')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='ScaledCoordinatesWrapped',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('x', models.FloatField()),
                ('y', models.FloatField()),
                ('z', models.FloatField()),
                ('scaledcoordinate', models.ForeignKey(to='results.ScaledCoordinate')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='StepCell',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('a', models.FloatField()),
                ('b', models.FloatField()),
                ('c', models.FloatField()),
                ('alpha', models.FloatField()),
                ('beta', models.FloatField()),
                ('gamma', models.FloatField()),
                ('mdstep', models.ForeignKey(to='results.MDStep')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='StepContributionsQM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('coreselfenergy', models.FloatField()),
                ('corehamiltonian', models.FloatField()),
                ('hartree', models.FloatField()),
                ('xc', models.FloatField()),
                ('hfx', models.FloatField()),
                ('dispersion', models.FloatField()),
                ('constraint', models.FloatField()),
                ('mdstep', models.ForeignKey(to='results.MDStep')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='StepEnergy',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('etot', models.FloatField()),
                ('epot', models.FloatField()),
                ('ekin', models.FloatField()),
                ('drift', models.FloatField()),
                ('mdstep', models.ForeignKey(to='results.MDStep')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='StepEnsemble',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('temperature', models.FloatField()),
                ('pressure', models.FloatField()),
                ('volume', models.FloatField()),
                ('conserved', models.FloatField()),
                ('mdstep', models.ForeignKey(to='results.MDStep')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='StepMetaQM',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('iasd', models.FloatField()),
                ('s2', models.FloatField()),
                ('scfcycles', models.FloatField()),
                ('otcycles', models.FloatField()),
                ('mdstep', models.ForeignKey(to='results.MDStep')),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.AddField(
            model_name='hirshfeldcharge',
            name='mdstep',
            field=models.ForeignKey(to='results.MDStep'),
        ),
        migrations.AddField(
            model_name='coordinate',
            name='mdstep',
            field=models.ForeignKey(to='results.MDStep'),
        ),
    ]
