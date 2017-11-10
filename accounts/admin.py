# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import UserInfo, RoleList, PermissionList

# Register your models here.

class UserInfoAdmin(admin.ModelAdmin):
    list_display = [
        'username',
        'nickname',
        'email',
        'is_active',
        'is_superuser',
        'role',

    ]



class PermissionListAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'url',

    ]

admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(PermissionList, PermissionListAdmin)