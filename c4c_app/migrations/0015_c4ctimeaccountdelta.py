# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('c4c_app', '0014_auto_20141205_1344'),
    ]

    operations = [
        migrations.CreateModel(
            name='C4CTimeAccountDelta',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, verbose_name='ID', serialize=False)),
                ('amount', models.IntegerField()),
                ('user', models.ForeignKey(to=settings.AUTH_USER_MODEL, related_name='time_account_deltas')),
            ],
            options={
                'verbose_name_plural': 'Time account deltas',
                'verbose_name': 'Time account delta',
            },
            bases=(models.Model,),
        ),
    ]
