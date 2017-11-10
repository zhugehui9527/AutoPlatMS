# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
# Create your models here.


# application/x-www-form-urlencoded   在发送前编码所有字符
# text/plain  空格转换为 "+" 加号，但不对特殊字符编码。

REQUEST_TYPE = (
    (1, 'application/json'),
    (2, 'text/plain'),
    (3, 'application/xml'),
    (4, 'application/rdf+xml'),
    (5, 'text/html'),
    (6, 'application/x-www-form-urlencoded'),
)

REQUEST_METHOD = (
    (1, 'GET'),
    (2, 'POST'),
)


RESPONSE_TYPE = (
    (1, 'json'),
    (2, 'text'),
    (3, 'xml'),
    (4, 'html'),

)


RESPONSE_STATUS = (
    (1, u"未执行"),
    (2, u"成功"),
    (3, u"失败"),
    (4, u"错误"),
)

IS_ACTIVE = (
    (1, u"启用"),
    (2, u"禁用"),
)


class CaseGroup(models.Model):
    '''定义用例的组别'''
    # unique 唯一，不允许重复
    name = models.CharField(u"组名", max_length=30, unique=True)
    # blank 针对表单，允许表单为空，null针对数据库，允许数据库该字段为空
    desc = models.CharField(U"描述", max_length=150, null=True, blank=True)

    def __unicode__(self):
        return self.name


class Case(models.Model):
    '''添加一条用例'''
    # csv文件表头名字科通通过verbose_name获取， 数据可以通过queryset语句来获取, Admin中显示的字段名称
    case_name = models.CharField(max_length=150, verbose_name=u"接口名称", error_messages={'required': u'接口名称不能为空'})
    url = models.URLField(max_length=600, verbose_name="URL", error_messages={'required': u'请求地址不能为空'})
    # ForeignKey 多对一,多条用例可以属于一个组,on_delete 外键删除，case_group如果被删除，则将该case_group设置为NULL
    case_group = models.ForeignKey(CaseGroup, verbose_name=u"用例属组", null=True, error_messages={'required': u'请选择一个属组'})
    request_method = models.IntegerField(u"请求方法", choices=REQUEST_METHOD, default=1)
    headers = models.CharField(u'请求头', max_length=1600, null=True, blank=True)
    params = models.CharField(u'请求参数', max_length=1600, null=True, blank=True)
    is_active = models.IntegerField(u"启用状态", choices=IS_ACTIVE, default=1)
    add_time = models.DateTimeField(u'添加时间', auto_now_add=True, editable=True)
    update_time = models.DateTimeField(u'更新时间', auto_now=True, null=True)
    expect_res = models.TextField(u'预期结果', max_length=2048, null=True, blank=True)
    response_code = models.TextField(u'响应码', max_length=50, null=True, blank=True)
    response_header = models.TextField(u'响应头', max_length=1600, null=True, blank=True)
    fact_res = models.TextField(u'结果响应', max_length=2048, null=True, blank=True)
    duration = models.CharField(u'执行耗时', max_length=50, null=True, blank=True, default='0')
    status = models.IntegerField(u"用例状态", choices=RESPONSE_STATUS, default=1)
    request_type = models.IntegerField(u"请求类型", choices=REQUEST_TYPE, default=1)
    remark = models.TextField(u'备注信息', max_length=2048, null=True, blank=True)

    def __unicode__(self):
        return self.case_name




















