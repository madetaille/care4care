# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0009_auto_20141203_0818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='c4cuser',
            name='branches',
        ),
    ]
