# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0013_auto_20141205_1119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cuser',
            name='avatar',
            field=models.ImageField(upload_to='avatars/', blank=True, default=None, null=True),
            preserve_default=True,
        ),
    ]
