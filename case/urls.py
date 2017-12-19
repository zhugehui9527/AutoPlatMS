# -*- coding: utf-8 -*-
from django.conf.urls import url, include
import case, api, group

urlpatterns = [
    url(r'case/$', case.case, name='case'),
    url(r'^case/add/$', case.case_add, name='case_add'),
    url(r'^case/del/$', case.case_del, name='case_del'),
    url(r'^case/run/$', case.case_run, name='case_run'),
    url(r'^case/info/(?P<ids>\d+)/$', case.case_info, name='case_info'),
    url(r'^case/edit/(?P<ids>\d+)/$', case.case_edit, name='case_edit'),
    url(r'^group/$', group.group, name='group'),
    url(r'^group/add/$', group.group_add, name='group_add'),
    url(r'^group/del/$', group.group_del, name='group_del'),
    url(r'^group/edit/(?P<ids>\d+)/$', group.group_edit, name='group_edit'),
    url(r'^group/save/$', group.group_save, name='group_save'),
    url(r'^api/get_case/$', api.get_case, name='get_case'),
    url(r'^api/index/update/$', api.update_index, name='update_index'),
]
