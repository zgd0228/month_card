# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-03-25 08:30
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0010_auto_20190325_1618'),
    ]

    operations = [
        migrations.AddField(
            model_name='vip',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='web.CardInfo', verbose_name='客户'),
        ),
        migrations.AlterField(
            model_name='cardinfo',
            name='end_time',
            field=models.DateField(default=datetime.datetime(2019, 4, 25, 16, 30, 52, 392043), verbose_name='截止日期'),
        ),
    ]
