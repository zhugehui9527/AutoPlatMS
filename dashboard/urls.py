# -*- coding: utf-8 -*-
from django.conf.urls import url, include
from dashboard.views import show_index

urlpatterns = [
    url(r'dashboard/index/$', show_index, name='dashboard_index'),

]
