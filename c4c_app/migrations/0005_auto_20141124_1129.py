# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('c4c_app', '0004_remove_c4cjob_complete'),
    ]

    operations = [
        migrations.AlterField(
            model_name='c4cjob',
            name='asked_by',
            field=models.ForeignKey(related_name='jobs_asked', default=None, blank=True, to='c4c_app.C4CUser', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cjob',
            name='done_by',
            field=models.ForeignKey(related_name='jobs_accepted', default=None, blank=True, to='c4c_app.C4CUser', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cjob',
            name='end_date',
            field=models.DateTimeField(default=None, null=True, blank=True),
            preserve_default=True,
        ),
    ]
