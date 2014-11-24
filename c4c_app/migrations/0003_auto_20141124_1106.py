# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0002_auto_20141124_1057'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cuser',
            name='branches',
            field=models.ManyToManyField(to='c4c_app.C4CBranch', blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cuser',
            name='network',
            field=models.ManyToManyField(to='c4c_app.C4CUser', blank=True),
            preserve_default=True,
        ),
    ]
