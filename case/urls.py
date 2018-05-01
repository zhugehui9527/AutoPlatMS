# -*- coding: utf-8 -*-
from django.conf.urls import url, include
# import case, api, group
from .case import *
from .api import *
from .group import *
from .report import report_template

urlpatterns = [
    url(r'case/$', case, name='case'),
    url(r'^case/add/$', case_add, name='case_add'),
    url(r'^case/del/$', case_del, name='case_del'),
    url(r'^case/run/$', case_run, name='case_run'),
    url(r'^case/info/(?P<ids>\d+)/$', case_info, name='case_info'),
    url(r'^case/edit/(?P<ids>\d+)/$', case_edit, name='case_edit'),
    url(r'^group/$', group, name='group'),
    url(r'^group/add/$', group_add, name='group_add'),
    url(r'^group/del/$', group_del, name='group_del'),
    url(r'^group/edit/(?P<ids>\d+)/$', group_edit, name='group_edit'),
    url(r'^group/info/(?P<ids>\d+)/$', group_info, name='group_info'),
    url(r'^group/run/$', group_run, name='group_run'),
    url(r'^group/result/$', group_result, name='group_result'),
    url(r'^group/result/del/$', result_del, name='result_del'),
    url(r'^group/save/$', group_save, name='group_save'),
    url(r'^api/getCase/$', get_case_info, name='get_case_info'),
    url(r'^api/getGroup/$', get_group, name='get_group'),
    url(r'^api/getGroupCase/$', getGroupCase, name='get_group_case'),
    url(r'^api/index/update/$', update_index, name='update_index'),
    url(r'^group/report/$', report_template, name='report_template'),




]
