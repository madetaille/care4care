# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0012_c4cuser_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cuser',
            name='avatar',
            field=models.ImageField(default=None, upload_to='avatars/', blank=True),
            preserve_default=True,
        ),
    ]
