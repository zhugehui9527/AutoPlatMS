# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-29 01:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mocks', '0002_mock_response'),
    ]

    operations = [
        migrations.AddField(
            model_name='mock',
            name='duration',
            field=models.CharField(blank=True, default='0', max_length=50, null=True, verbose_name='\u6267\u884c\u8017\u65f6'),
        ),
    ]
