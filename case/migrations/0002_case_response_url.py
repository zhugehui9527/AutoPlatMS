# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-05-02 06:03
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('case', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='case',
            name='response_url',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='响应URL'),
        ),
    ]
