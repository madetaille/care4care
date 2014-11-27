# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0001_initial'),
        ('c4c_app', '0006_c4cjob_complete'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='c4cbranch',
            options={'verbose_name': 'Branch', 'verbose_name_plural': 'Branches'},
        ),
        migrations.AlterModelOptions(
            name='c4cdonation',
            options={'verbose_name': 'Donation', 'verbose_name_plural': 'Donations'},
        ),
        migrations.AlterModelOptions(
            name='c4cevent',
            options={'verbose_name': 'Event', 'verbose_name_plural': 'Events'},
        ),
        migrations.AlterModelOptions(
            name='c4cjob',
            options={'verbose_name': 'Job', 'verbose_name_plural': 'Jobs'},
        ),
        migrations.AlterModelOptions(
            name='c4cuser',
            options={'verbose_name': 'C4C User', 'verbose_name_plural': 'C4C Users'},
        ),
        migrations.RemoveField(
            model_name='c4cbranch',
            name='officers',
        ),
        migrations.AddField(
            model_name='c4cbranch',
            name='group',
            field=models.OneToOneField(related_name='in_branches', default=None, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='c4cbranch',
            name='officers_group',
            field=models.OneToOneField(related_name='is_branch_officer_of', default=None, to='auth.Group'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='c4cjob',
            name='offer',
            field=models.BooleanField(default=False),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='c4cjob',
            name='duration',
            field=models.IntegerField(null=True),
            preserve_default=True,
        ),
    ]
