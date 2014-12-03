# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('c4c_app', '0008_auto_20141127_1038'),
    ]

    operations = [
        migrations.CreateModel(
            name='C4CNews',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, verbose_name='ID', auto_created=True)),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField()),
                ('description', models.CharField(max_length=1000)),
                ('branch', models.ForeignKey(null=True, blank=True, default=None, to='c4c_app.C4CBranch')),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
            bases=(models.Model,),
        ),
        migrations.AlterField(
            model_name='c4cjob',
            name='duration',
            field=models.IntegerField(null=True, blank=True, default=0),
            preserve_default=True,
        ),
    ]
