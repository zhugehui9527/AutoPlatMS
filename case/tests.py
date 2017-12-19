# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.

import requests

#
# url1 = ''
# data1 = ''
#
# url11 = ''
# data11 = ''
#
# s = requests.session()
#
# r1 = s.get(url=url1)
# r1.content
#
# r2 = s.post(url=url11, data=data11)
# r2.content

request = 'task'
print getattr(request, 'task', None) if request else None


a = None
print sum(range(10),3) if a else None

tasks = [1, 3]
print zip(tasks, tasks)


list1 = range(10)

b = list(x for x in list1 if x!=1)
print b
