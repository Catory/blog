# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-12-26 09:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0004_auto_20171216_1750'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='posts',
            options={'ordering': ['-ptime']},
        ),
        migrations.AddField(
            model_name='user',
            name='confirmed',
            field=models.BooleanField(default=0),
        ),
        migrations.AlterField(
            model_name='posts',
            name='ptitle',
            field=models.CharField(default=' ', max_length=50),
        ),
    ]
