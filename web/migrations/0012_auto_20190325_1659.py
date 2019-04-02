# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-03-25 08:59
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0011_auto_20190325_1630'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='game',
            name='vip',
        ),
        migrations.RemoveField(
            model_name='vip',
            name='user',
        ),
        migrations.AddField(
            model_name='cardinfo',
            name='vip',
            field=models.ManyToManyField(to='web.Vip'),
        ),
        migrations.AddField(
            model_name='vip',
            name='game',
            field=models.ManyToManyField(to='web.Game'),
        ),
        migrations.AlterField(
            model_name='cardinfo',
            name='end_time',
            field=models.DateField(default=datetime.datetime(2019, 4, 25, 16, 59, 23, 648315), verbose_name='截止日期'),
        ),
    ]
