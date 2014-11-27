# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0007_auto_20141127_0941'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cbranch',
            name='main_user',
            field=models.OneToOneField(to=settings.AUTH_USER_MODEL, related_name='is_main_user_of_branch'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cbranch',
            name='name',
            field=models.CharField(primary_key=True, max_length=60, serialize=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cdonation',
            name='receiver',
            field=models.ForeignKey(related_name='donations_received', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cdonation',
            name='sender',
            field=models.ForeignKey(related_name='donations_made', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cevent',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cjob',
            name='asked_by',
            field=models.ForeignKey(blank=True, default=None, null=True, to=settings.AUTH_USER_MODEL, related_name='jobs_asked'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cjob',
            name='created_by',
            field=models.ForeignKey(related_name='jobs_created', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cjob',
            name='done_by',
            field=models.ForeignKey(blank=True, default=None, null=True, to=settings.AUTH_USER_MODEL, related_name='jobs_accepted'),
            preserve_default=True,
        ),
    ]
