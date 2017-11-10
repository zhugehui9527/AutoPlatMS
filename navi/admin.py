# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import navi

# Register your models here.


class NaviAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'description',
        'url',
    ]

admin.site.register(navi, NaviAdmin)
