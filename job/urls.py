# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from . import jobs, views

urlpatterns = [
    url(r'^job/list/$', jobs.index, name='job_list'),
    url(r'^job/add/$', jobs.job_add, name='job_add'),
    url(r'^job/edit/(?P<ids>\d+)/$', jobs.job_edit, name='job_edit'),
    url(r'^job/del/$', jobs.job_del, name='job_del'),
    url(r'^interval/list/$', jobs.job_interval_list, name='job_interval_list'),
    url(r'^interval/del/$', jobs.job_interval_del, name='job_interval_del'),
    url(r'^interval/add/$', jobs.job_interval_add, name='job_interval_add'),
    url(r'^interval/edit/(?P<ids>\d+)/$', jobs.job_interval_edit, name='job_interval_edit'),
    url(r'^crontab/list/$', jobs.job_crontab_list, name='job_crontab_list'),
    url(r'^crontab/del/$', jobs.job_crontab_del, name='job_crontab_del'),
    url(r'^crontab/add/$', jobs.job_crontab_add, name='job_crontab_add'),
    url(r'^crontab/edit/(?P<ids>\d+)/$', jobs.job_crontab_edit, name='job_crontab_edit'),
    url(r'^result/list/$', jobs.job_result_list, name='job_result_list'),
    url(r'^result/edit/(?P<ids>\d+)/$', jobs.job_result_edit, name='job_result_edit'),
    url(r'^result/del/$', jobs.job_result_del, name='job_result_del'),
    url(r'^job/backend/$', jobs.job_backend, name='job_backend'),
    url(r'^job/backend/task/(?P<name>\w+)/(?P<action>\w+)$', jobs.job_backend_task, name='job_backend_task'),
    url(r'^job/view/$', views.task_test, name='job_view')
]