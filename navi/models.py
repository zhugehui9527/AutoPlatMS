# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.


class navi(models.Model):
    name = models.CharField(u"名称", max_length=150)
    description = models.CharField(u"描述", max_length=150)
    url = models.URLField(u'网址')

    def __unicode__(self):
        return self.name
