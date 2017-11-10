# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Case

# Register your models here.

class CaseAdmin(admin.ModelAdmin):
    list_display = [
        'case_name',
        'url',
        'case_group',
        'request_method',
        'headers',
        'params',
        'is_active',
        'add_time',
        'update_time',
        'expect_res',
        'response_code',
        'response_header',
        'fact_res',
        'duration',
        'status',
        'remark',

    ]

admin.site.register(Case, CaseAdmin)