# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-03-31 00:34
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0024_auto_20190331_0033'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cardinfo',
            name='end_time',
            field=models.DateField(default=datetime.datetime(2019, 5, 1, 0, 34, 25, 472800), verbose_name='截止日期'),
        ),
    ]
