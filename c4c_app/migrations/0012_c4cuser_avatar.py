# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0011_auto_20141203_1415'),
    ]

    operations = [
        migrations.AddField(
            model_name='c4cuser',
            name='avatar',
            field=models.ImageField(upload_to='avatars/', default=None),
            preserve_default=False,
        ),
    ]
