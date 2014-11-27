# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0008_auto_20141127_1038'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cjob',
            name='duration',
            field=models.IntegerField(default=0, null=True, blank=True),
            preserve_default=True,
        ),
    ]
