# -*- coding: utf-8 -*-
from django.conf.urls import url, include

from .views import *

urlpatterns = [

    # mock api 路径正则表达式
    url(r'^mock_api/(?P<path>[\w/.?=@#$%&-]+)', mock_api, name='mock_api'),
    url(r'^add/$', mock_add, name='mock_add'),
    url(r'^del/$', mock_del, name='mock_del'),
    url(r'^index/$', mock_index, name='mock_index'),
    url(r'^info/(?P<ids>\d+)/$', mock_run, name='mock_run'),
    url(r'^edit/(?P<ids>\d+)/$', mock_edit, name='mock_edit'),
    url(r'^mock_index/$', mock_index, name='mock_index'),
    url(r'^group/index/$', group, name='mock_group_index'),
    url(r'^group/add/$', group_add, name='mock_group_add'),
    url(r'^group/del/$', group_del, name='mock_group_del'),
    url(r'^group/edit/(?P<ids>\d+)/$', group_edit, name='mock_group_edit'),
    url(r'^group/save/$', group_save, name='mock_group_save'),

]

