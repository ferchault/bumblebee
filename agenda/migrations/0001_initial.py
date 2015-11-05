# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import bumblebee.models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=45)),
                ('active', models.BooleanField()),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='TodoEntry',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('task', models.CharField(max_length=200)),
                ('duedate', models.DateField()),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='TodoPriority',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=20)),
                ('priority', models.IntegerField()),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.CreateModel(
            name='TodoStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=30)),
                ('completed', models.BooleanField()),
            ],
            bases=(models.Model, bumblebee.models.ExplainableMixin),
        ),
        migrations.AddField(
            model_name='todoentry',
            name='priority',
            field=models.ForeignKey(to='agenda.TodoPriority'),
        ),
        migrations.AddField(
            model_name='todoentry',
            name='project',
            field=models.ForeignKey(to='agenda.Project'),
        ),
        migrations.AddField(
            model_name='todoentry',
            name='status',
            field=models.ForeignKey(to='agenda.TodoStatus'),
        ),
    ]
