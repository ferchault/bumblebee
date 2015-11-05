# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import bumblebee.models


class Migration(migrations.Migration):

    dependencies = [
        ('results', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='SeriesAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=45)),
                ('value', models.CharField(max_length=100)),
                ('series', models.ForeignKey(to='results.Series')),
            ],
            bases=(models.Model, bumblebee.models.Explainable),
        ),
        migrations.CreateModel(
            name='SinglePointAttributes',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('key', models.CharField(max_length=45)),
                ('value', models.CharField(max_length=100)),
                ('series', models.ForeignKey(to='results.Series')),
            ],
            bases=(models.Model, bumblebee.models.Explainable),
        ),
        migrations.AlterField(
            model_name='system',
            name='name',
            field=models.CharField(help_text=b'Unique name of the physical system treated in this simulation.', max_length=45),
        ),
    ]
