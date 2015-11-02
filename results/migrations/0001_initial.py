# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Bucket',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('token', models.CharField(max_length=50)),
                ('comment', models.CharField(max_length=200)),
                ('updated', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('bucket', models.ForeignKey(to='results.Bucket')),
            ],
        ),
        migrations.CreateModel(
            name='SinglePoint',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('series', models.ForeignKey(to='results.Series')),
            ],
        ),
        migrations.CreateModel(
            name='SinglePointOuter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('lagrangian', models.FloatField()),
                ('orderparameter', models.FloatField()),
                ('gradient', models.FloatField()),
                ('scfcycles', models.IntegerField()),
                ('otnumber', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='System',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
            ],
        ),
        migrations.AddField(
            model_name='bucket',
            name='system',
            field=models.ForeignKey(to='results.System'),
        ),
    ]
