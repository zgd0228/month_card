# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-03-25 08:18
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_auto_20190325_1618'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardinfo',
            name='end_time',
            field=models.DateField(default=datetime.datetime(2019, 4, 25, 16, 18, 12, 865860), verbose_name='截止日期'),
        ),
        migrations.AlterField(
            model_name='vip',
            name='title',
            field=models.CharField(default=1, max_length=32, verbose_name='vip'),
        ),
    ]
