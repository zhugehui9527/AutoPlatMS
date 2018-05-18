# -*- coding:utf-8 -*-
from django import forms
from django.forms.widgets import *
from .models import CaseGroup, Case


class CaseForm(forms.ModelForm):
    '''接口表单'''
    class Meta:
        ''' 模型表单 '''
        model = Case
        # exclude 除了这些不用渲染
        exclude = ("id", "add_time", "status", "duration", "fact_res", "NO", "traceback", "response_url")
        # widgets 用来渲染成HTML元素的工具
        widgets = {
            'path': TextInput(
                attrs={'class': 'form-control', 'style': 'width:530px',
                       'placeholder': u'请填写接口请求路径,比如: /casemanage/case/add/'}),
            'protocol': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'ip': TextInput(
                attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写域名或者ip'}),
            'port': TextInput(
                attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写端口,http默认80，https默认443'}),
            'case_name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写接口名称,比如：登录接口测试'}),
            'case_group': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'request_method': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'headers': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写请求头,注意格式：{}'}),
            'params': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写请求参数'}),
            'is_active': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'add_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'update_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'expect_res': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写预期结果断言'}),
            # 'response_url': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'fact_res': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'readonly': True}),
            'request_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'remark': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写备注信息'}),
            'proxies': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'eg：http://127.0.0.1:8000'}),
        }


class GroupForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(GroupForm, self).clean()
        value = cleaned_data.get('name')
        try:
            CaseGroup.objects.get(name=value)
            self._errors['name'] = self.error_class(['%s 的信息已经存在' % value])
        except CaseGroup.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = CaseGroup
        exclude = ("id", 'update_time', 'add_time', 'duration', 'status' )
        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control',
                       'style': 'width:480px',
                       'placeholder': u'请填写组名',
                       # 'data-toggle': 'tooltip',
                       # 'title': '组名',
                       }),
            'desc': TextInput(
                attrs={'class': 'form-control', 'style': 'width:480px',
                       'placeholder': u'请填写描述'}),
            'protocol': Select(attrs={'class': 'form-control', 'style': 'width:480px;'}),
            'ip': TextInput(
                attrs={'class': 'form-control', 'style': 'width:480px;', 'placeholder': u'请填写域名或者ip'}),
            'port': TextInput(
                attrs={'class': 'form-control', 'style': 'width:480px;', 'placeholder': u'请填写端口'}),
            'rerun': NumberInput(
                attrs={'class': 'form-control', 'style': 'width:480px;'}),
            'proxies': TextInput(
                attrs={'class': 'form-control', 'style': 'width:480px;', 'placeholder': u'请填写代理：http://127.0.0.1:8000'}),
            # 'add_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'update_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'duration': TextInput(attrs={'class': 'form-control', 'style': 'width:100px;'}),

        }






















