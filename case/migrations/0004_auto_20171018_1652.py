# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-18 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0003_auto_20171018_1620'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='response_code',
            field=models.TextField(blank=True, max_length=50, null=True, verbose_name='\u54cd\u5e94\u7801'),
        ),
        migrations.AddField(
            model_name='case',
            name='response_header',
            field=models.TextField(blank=True, max_length=600, null=True, verbose_name='\u54cd\u5e94\u5934'),
        ),
    ]
