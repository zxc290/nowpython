# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-09 14:11
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0027_auto_20171209_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='nickname',
            field=models.CharField(default='123', max_length=30, verbose_name='昵称'),
        ),
    ]
