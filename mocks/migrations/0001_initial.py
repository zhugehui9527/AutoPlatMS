# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-03-28 07:35
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Mock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='\u63a5\u53e3\u540d\u79f0')),
                ('request_method', models.IntegerField(choices=[(1, 'GET'), (2, 'POST')], default=1, verbose_name='\u8bf7\u6c42\u65b9\u6cd5')),
                ('path', models.CharField(blank=True, max_length=600, null=True, verbose_name='\u8def\u5f84')),
                ('headers', models.CharField(blank=True, max_length=1600, null=True, verbose_name='\u8bf7\u6c42\u5934')),
                ('params', models.CharField(blank=True, max_length=1600, null=True, verbose_name='\u8bf7\u6c42\u53c2\u6570')),
                ('status', models.IntegerField(choices=[(1, '\u672a\u5b8c\u6210'), (2, '\u5df2\u5b8c\u6210')], default=1, null=True, verbose_name='\u7f16\u8f91\u72b6\u6001')),
                ('create_user', models.CharField(max_length=200, verbose_name='\u521b\u5efa\u7528\u6237')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('is_active', models.IntegerField(choices=[(1, '\u542f\u7528'), (2, '\u7981\u7528')], default=1, verbose_name='\u542f\u7528\u72b6\u6001')),
                ('remark', models.TextField(blank=True, max_length=2048, null=True, verbose_name='\u5907\u6ce8\u4fe1\u606f')),
            ],
        ),
        migrations.CreateModel(
            name='MockGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('protocol', models.IntegerField(choices=[(0, None), (1, 'http'), (2, 'https')], default=1, null=True, verbose_name='\u534f\u8bae')),
                ('ip', models.CharField(blank=True, max_length=150, null=True, verbose_name='\u57df\u540d')),
                ('port', models.CharField(blank=True, max_length=150, null=True, verbose_name='\u7aef\u53e3')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='\u5c5e\u7ec4\u540d\u79f0')),
                ('desc', models.TextField(blank=True, max_length=1600, null=True, verbose_name='\u63cf\u8ff0')),
            ],
        ),
        migrations.AddField(
            model_name='mock',
            name='group',
            field=models.ForeignKey(error_messages={'required': '\u8bf7\u9009\u62e9\u4e00\u4e2a\u5c5e\u7ec4'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='mocks.MockGroup', verbose_name='\u5c5e\u7ec4'),
        ),
    ]
