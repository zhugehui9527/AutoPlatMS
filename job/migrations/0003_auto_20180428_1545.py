# -*- coding: utf-8 -*-
# Generated by Django 1.11.12 on 2018-04-28 07:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('job', '0002_auto_20180428_1505'),
    ]

    operations = [
        migrations.AlterField(
            model_name='emailmanager',
            name='eamil_config',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='config.EmailConfig'),
        ),
    ]