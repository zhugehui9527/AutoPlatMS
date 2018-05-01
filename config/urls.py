"""AutoPlatMS URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from config import views


urlpatterns = [
    url(r'^$', views.index, name='config'),
    url(r'^config_save/$', views.config_save, name='config_save'),
    url(r'^token/$', views.get_token, name='token'),
    url(r'^email/list/$', views.email_list, name='email_list'),
    url(r'^email/add/$', views.email_add, name='email_add'),
    url(r'^email/edit/(?P<ids>\d+)/$', views.email_edit, name='email_edit'),
    url(r'^email/del/(?P<ids>\d+)/$', views.email_del, name='email_del'),

]
