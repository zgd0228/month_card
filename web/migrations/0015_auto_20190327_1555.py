# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-03-27 07:55
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0014_auto_20190327_1550'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardinfo',
            name='end_time',
            field=models.DateField(default=datetime.datetime(2019, 4, 27, 15, 55, 15, 628692), verbose_name='截止日期'),
        ),
        migrations.AlterField(
            model_name='time',
            name='tm',
            field=models.CharField(max_length=32),
        ),
    ]
