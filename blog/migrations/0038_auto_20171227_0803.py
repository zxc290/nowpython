# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-27 00:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0037_auto_20171227_0801'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='评论内容'),
        ),
    ]
