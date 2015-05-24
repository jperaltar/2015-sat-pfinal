# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activities',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=128)),
                ('eventType', models.CharField(max_length=128)),
                ('price', models.CharField(max_length=16)),
                ('time', models.DateTimeField()),
                ('duration', models.CharField(max_length=128)),
                ('longDuration', models.IntegerField()),
                ('description', models.CharField(max_length=256)),
                ('score', models.IntegerField(default=0)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('user', models.CharField(max_length=32)),
                ('comment', models.TextField()),
                ('activity', models.ForeignKey(to='cultural.Activities')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='lastUpdate',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True)),
                ('time', models.DateTimeField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User_Activity',
            fields=[
                ('user', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('title', models.CharField(max_length=32, blank=True)),
                ('description', models.TextField(blank=True)),
                ('colour', models.CharField(max_length=32, blank=True)),
                ('activity', models.ManyToManyField(to='cultural.Activities', null=True, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='userTime',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('time', models.DateTimeField()),
                ('user', models.CharField(max_length=32)),
                ('activityID', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
