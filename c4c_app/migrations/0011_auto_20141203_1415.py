# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0010_remove_c4cuser_branches'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cnews',
            name='description',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cnews',
            name='title',
            field=models.CharField(max_length=200),
            preserve_default=True,
        ),
    ]
