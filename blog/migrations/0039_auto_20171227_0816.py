# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-27 00:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0038_auto_20171227_0803'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(blank=True, null=True, verbose_name='评论内容'),
        ),
    ]
