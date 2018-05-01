# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from djcelery.compat import python_2_unicode_compatible


@python_2_unicode_compatible
class EmailConfig(models.Model):
    '''邮件配置'''
    email_user = models.EmailField(u'邮箱账号', max_length=255)
    email_pwd = models.CharField(u'邮箱密码', max_length=200)
    email_host = models.CharField(u'邮箱域名', max_length=200)
    email_port = models.IntegerField(u'邮箱端口', default=25)
    email_ssl = models.BooleanField(u'邮箱SSL')

    def __str__(self):
        return self.email_user