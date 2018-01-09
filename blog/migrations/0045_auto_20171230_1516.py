# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-30 07:16
from __future__ import unicode_literals

from django.db import migrations
import imagekit.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0044_post_cover'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='cover',
            field=imagekit.models.fields.ProcessedImageField(default='cover/default_cover.jpg', upload_to='cover', verbose_name='封面'),
        ),
    ]
