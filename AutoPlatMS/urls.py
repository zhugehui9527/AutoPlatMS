# -*- coding: utf-8 -*-
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
from django.contrib import admin
from .views import index

from accounts.models import UserInfo
from rest_framework import routers, serializers, viewsets


# Serializers定义了API的表现.
class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserInfo
        fields = ('username', 'email', 'is_superuser')


# ViewSets 定义了 视图（view） 的行为.
class UserViewSet(viewsets.ModelViewSet):
    queryset = UserInfo.objects.all()
    serializer_class = UserSerializer


# Routers 提供了一种简单途径，自动地配置了URL。
router = routers.DefaultRouter()
router.register(r'users', UserViewSet)

# 使用自动的URL路由，让我们的API跑起来。
# 此外，我们也包括了登入可视化API的URLs。
urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('accounts.urls')),
    url(r'^navi/', include('navi.urls')),
    url(r'^dash/', include('dashboard.urls')),
    url(r'^casemanage/', include('case.urls')),
    url(r'^jobs/', include('job.urls')),
    url(r'^config/', include('config.urls')),
    url(r'^mock/', include('mocks.urls')),
    url(r'^api-auth/', include('rest_framework.urls')),
    url(r'^rest/', include(router.urls)),


]
