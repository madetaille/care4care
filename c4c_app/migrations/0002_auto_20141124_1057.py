# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cuser',
            name='branches',
            field=models.ManyToManyField(default=None, to='c4c_app.C4CBranch', null=True),
            preserve_default=True,
        ),
    ]
