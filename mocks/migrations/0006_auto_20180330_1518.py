# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-30 07:18
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocks', '0005_auto_20180329_1951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mock',
            options={'ordering': ['-update_time']},
        ),
        migrations.AddField(
            model_name='mock',
            name='mock_path',
            field=models.CharField(blank=True, max_length=240, null=True, verbose_name='Mock\u5730\u5740'),
        ),
        migrations.AlterField(
            model_name='mock',
            name='path',
            field=models.CharField(max_length=240, unique=True, verbose_name='\u8def\u5f84'),
        ),
    ]
