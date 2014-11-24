# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0005_auto_20141124_1129'),
    ]

    operations = [
        migrations.AddField(
            model_name='c4cjob',
            name='complete',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
    ]
