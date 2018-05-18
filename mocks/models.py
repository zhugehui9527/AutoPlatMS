# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from djcelery.compat import python_2_unicode_compatible
# Create your models here.

_STATUS = (
    (1, '未完成'),
    (2, '已完成')

)

REQUEST_METHOD = (
    (1, 'GET'),
    (2, 'POST'),
)


PROTOCOL = (
    (0, None),
    (1, 'http'),
    (2, 'https'),
)

IS_ACTIVE = (
    (1, u"启用"),
    (2, u"禁用"),
)


@python_2_unicode_compatible
class MockGroup(models.Model):
    '''mock 属组管理'''
    name = models.CharField('属组名称', max_length=200, unique=True)
    create_time = models.DateTimeField(u'添加时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
    # protocol = models.IntegerField(u"协议", choices=PROTOCOL, null=True, default=1)
    # ip = models.CharField(max_length=150, verbose_name="域名", null=True, blank=True)
    # port = models.CharField(max_length=150, verbose_name="端口", null=True, blank=True)
    desc = models.TextField(U"描述", max_length=1600, null=True, blank=True)

    # def __unicode__(self):
    #     '''美化group name，如果不添加 Mock.group 获取不到名字'''
    #     return self.name

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Mock(models.Model):
    '''mock model'''
    name = models.CharField('接口名称', max_length=200, unique=True)
    request_method = models.IntegerField(u"请求方法", choices=REQUEST_METHOD, default=1)
    path = models.CharField(max_length=240, verbose_name="路径", unique=True)
    headers = models.TextField(u'请求头', max_length=1600, null=True, blank=True)
    params = models.TextField(u'请求参数', max_length=1600, null=True, blank=True)
    status = models.IntegerField(u"编辑状态", choices=_STATUS, null=True, default=1)
    create_user = models.CharField('创建用户', max_length=200)
    create_time = models.DateTimeField(u'添加时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
    duration = models.CharField(u'执行耗时', max_length=50, null=True, blank=True, default='0')
    group = models.ForeignKey(MockGroup, on_delete=models.CASCADE, verbose_name=u"属组", null=True,
                              error_messages={'required': u'请选择一个属组'},
                              ) # 级连删除on_delete=models.CASCADE
    is_active = models.IntegerField(u"启用状态", choices=IS_ACTIVE, default=1)
    remark = models.TextField(u'备注信息', max_length=2048, null=True, blank=True)
    response = models.TextField(u'响应信息', null=True, blank=True)
    # response_headers = models.TextField(u'响应头', max_length=1600, null=True, blank=True)
    mock_path = models.CharField('Mock地址', max_length=240, null=True, blank=True)


    # def __unicode__(self):
    #     return self.name

    def __str__(self):
        return self.name

    # class Meta:
    #     '''按照用例的名字进行排序,倒序只需要加 -'''
    #     ordering = ['-update_time']




