# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from djcelery.models import TaskState, PeriodicTask, TaskMeta
from config.models import EmailConfig
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from djcelery.compat import python_2_unicode_compatible


@python_2_unicode_compatible
class EmailManager(models.Model):
    '''邮件管理器'''
    email_enbale = models.BooleanField(u'邮件禁用')
    email_subiect = models.CharField(u'邮件主题', max_length=200)
    email_message = models.TextField(u'邮件信息')
    email_to = models.CharField(u'收件人', max_length=200)
    email_cc = models.CharField(u'抄送', max_length=400, blank=True)
    email_bcc = models.CharField(u'密送', max_length=400, blank=True)
    eamil_config = models.ForeignKey(to=EmailConfig, verbose_name=u'发件人')
    email_periodictask = models.OneToOneField(verbose_name=u'定时任务', to=PeriodicTask, related_name='periodictask_email')

    def __str__(self):
        return self.email_user




