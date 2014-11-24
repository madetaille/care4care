# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='C4CBranch',
            fields=[
                ('name', models.CharField(max_length=100, serialize=False, primary_key=True)),
                ('address', models.CharField(max_length=300)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='C4CDonation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date', models.DateTimeField()),
                ('message', models.CharField(max_length=1000)),
                ('amount', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='C4CEvent',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=1000)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='C4CJob',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=1000)),
                ('duration', models.IntegerField()),
                ('location', models.CharField(max_length=300)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('complete', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='C4CUser',
            fields=[
                ('user', models.OneToOneField(primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('address', models.CharField(max_length=300)),
                ('time_account', models.IntegerField(default=0)),
                ('birthday', models.DateField()),
                ('branches', models.ManyToManyField(to='c4c_app.C4CBranch')),
                ('network', models.ManyToManyField(to='c4c_app.C4CUser')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='c4cjob',
            name='asked_by',
            field=models.ForeignKey(related_name='jobs_asked', default=None, to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cjob',
            name='created_by',
            field=models.ForeignKey(related_name='jobs_created', to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cjob',
            name='done_by',
            field=models.ForeignKey(related_name='jobs_accepted', default=None, to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cevent',
            name='job',
            field=models.ForeignKey(default=None, blank=True, to='c4c_app.C4CJob', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cevent',
            name='user',
            field=models.ForeignKey(to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cdonation',
            name='receiver',
            field=models.ForeignKey(related_name='donations_received', to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cdonation',
            name='sender',
            field=models.ForeignKey(related_name='donations_made', to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cbranch',
            name='main_user',
            field=models.OneToOneField(related_name='is_main_user_of_branch', to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='c4cbranch',
            name='officers',
            field=models.ManyToManyField(to='c4c_app.C4CUser'),
            preserve_default=True,
        ),
    ]
