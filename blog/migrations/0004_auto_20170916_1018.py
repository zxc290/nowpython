# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-16 02:18
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_comments'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comments',
            options={'verbose_name': '评论', 'verbose_name_plural': '评论'},
        ),
    ]
