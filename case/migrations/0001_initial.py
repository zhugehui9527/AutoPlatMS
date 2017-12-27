# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-26 02:37
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('case_name', models.CharField(error_messages={'required': '\u63a5\u53e3\u540d\u79f0\u4e0d\u80fd\u4e3a\u7a7a'}, max_length=150, verbose_name='\u63a5\u53e3\u540d\u79f0')),
                ('path', models.CharField(blank=True, max_length=600, null=True, verbose_name='\u8def\u5f84')),
                ('protocol', models.IntegerField(choices=[(0, None), (1, 'http'), (2, 'https')], default=0, verbose_name='\u534f\u8bae')),
                ('ip', models.CharField(blank=True, max_length=150, null=True, verbose_name='\u57df\u540d')),
                ('port', models.CharField(blank=True, max_length=150, null=True, verbose_name='\u7aef\u53e3')),
                ('request_method', models.IntegerField(choices=[(1, 'GET'), (2, 'POST')], default=1, verbose_name='\u8bf7\u6c42\u65b9\u6cd5')),
                ('headers', models.CharField(blank=True, max_length=1600, null=True, verbose_name='\u8bf7\u6c42\u5934')),
                ('params', models.CharField(blank=True, max_length=1600, null=True, verbose_name='\u8bf7\u6c42\u53c2\u6570')),
                ('is_active', models.IntegerField(choices=[(1, '\u542f\u7528'), (2, '\u7981\u7528')], default=1, verbose_name='\u542f\u7528\u72b6\u6001')),
                ('add_time', models.DateTimeField(auto_now_add=True, verbose_name='\u6dfb\u52a0\u65f6\u95f4')),
                ('update_time', models.DateTimeField(auto_now=True, null=True, verbose_name='\u66f4\u65b0\u65f6\u95f4')),
                ('expect_res', models.TextField(blank=True, max_length=2048, null=True, verbose_name='\u9884\u671f\u7ed3\u679c')),
                ('response_code', models.TextField(blank=True, max_length=50, null=True, verbose_name='\u54cd\u5e94\u7801')),
                ('response_header', models.TextField(blank=True, max_length=1600, null=True, verbose_name='\u54cd\u5e94\u5934')),
                ('fact_res', models.TextField(blank=True, max_length=2048, null=True, verbose_name='\u7ed3\u679c\u54cd\u5e94')),
                ('duration', models.CharField(blank=True, default='0', max_length=50, null=True, verbose_name='\u6267\u884c\u8017\u65f6')),
                ('status', models.IntegerField(choices=[(1, '\u672a\u6267\u884c'), (2, '\u6210\u529f'), (3, '\u5931\u8d25'), (4, '\u9519\u8bef')], default=1, verbose_name='\u7528\u4f8b\u72b6\u6001')),
                ('request_type', models.IntegerField(choices=[(1, 'application/json'), (2, 'text/plain'), (3, 'application/xml'), (4, 'application/rdf+xml'), (5, 'text/html'), (6, 'application/x-www-form-urlencoded')], default=1, verbose_name='\u8bf7\u6c42\u7c7b\u578b')),
                ('remark', models.TextField(blank=True, max_length=2048, null=True, verbose_name='\u5907\u6ce8\u4fe1\u606f')),
                ('proxies', models.CharField(blank=True, default='', max_length=250, null=True, verbose_name='\u4ee3\u7406')),
                ('NO', models.IntegerField(default=0, verbose_name='\u5e8f\u53f7')),
            ],
            options={
                'ordering': ['NO'],
            },
        ),
        migrations.CreateModel(
            name='CaseGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True, verbose_name='\u7ec4\u540d')),
                ('desc', models.CharField(blank=True, max_length=150, null=True, verbose_name='\u63cf\u8ff0')),
                ('proxies', models.CharField(blank=True, max_length=250, null=True, verbose_name='\u4ee3\u7406')),
                ('protocol', models.IntegerField(choices=[(0, None), (1, 'http'), (2, 'https')], default=0, null=True, verbose_name='\u534f\u8bae')),
                ('ip', models.CharField(blank=True, max_length=150, null=True, verbose_name='\u57df\u540d')),
                ('port', models.CharField(blank=True, max_length=150, null=True, verbose_name='\u7aef\u53e3')),
            ],
        ),
        migrations.AddField(
            model_name='case',
            name='case_group',
            field=models.ForeignKey(error_messages={'required': '\u8bf7\u9009\u62e9\u4e00\u4e2a\u5c5e\u7ec4'}, null=True, on_delete=django.db.models.deletion.CASCADE, to='case.CaseGroup', verbose_name='\u7528\u4f8b\u5c5e\u7ec4'),
        ),
    ]
