# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2019-03-22 03:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, verbose_name='用户姓名')),
                ('pwd', models.CharField(default='', max_length=64, verbose_name='密码')),
                ('roles', models.ManyToManyField(to='rbac.Role', verbose_name='用户角色')),
            ],
        ),
    ]
