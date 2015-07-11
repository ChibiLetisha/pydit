# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('linkaggregator', '0006_auto_20150701_1032'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='comments',
            field=models.ManyToManyField(to='linkaggregator.Comment', blank=True),
        ),
        migrations.AlterField(
            model_name='post',
            name='votes',
            field=models.ManyToManyField(to='linkaggregator.Vote', blank=True),
        ),
    ]
