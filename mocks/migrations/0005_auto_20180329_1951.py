# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-29 11:51
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocks', '0004_auto_20180329_1617'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='mock',
            options={'ordering': ['update_time']},
        ),
        migrations.AlterField(
            model_name='mock',
            name='response',
            field=models.TextField(blank=True, null=True, verbose_name='\u54cd\u5e94\u4fe1\u606f'),
        ),
    ]
