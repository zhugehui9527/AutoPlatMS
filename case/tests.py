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

a = [1, 3, 2]
dict1 = {
    'a':1,
    'b':2
}

dict2 = {

}

for i in a:
    dict2[i] = dict1

print(dict2)