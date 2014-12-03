# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('c4c_app', '0009_auto_20141127_1521'),
    ]

    operations = [
        migrations.CreateModel(
            name='C4CNews',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=1000)),
                ('branch', models.ForeignKey(to='c4c_app.C4CBranch', blank=True, null=True, default=None)),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'News',
                'verbose_name': 'News',
            },
            bases=(models.Model,),
        ),
    ]
