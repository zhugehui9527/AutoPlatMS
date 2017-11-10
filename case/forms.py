# -*- coding:utf-8 -*-
from django import forms
from django.forms.widgets import *
from .models import CaseGroup, Case


class CaseForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(CaseForm, self).clean()
        params = cleaned_data.get('params')
        print params
        return cleaned_data

    class Meta:
        ''' 模型表单 '''
        model = Case
        exclude = ("id", "status",)
        # widgets 用来渲染成HTML元素的工具
        widgets = {
            'url': URLInput(attrs={'class': 'form-control', 'style': 'width:530px', 'placeholder': u'请填写接口请求地址,比如: http://127.0.0.1:8000/casemanage/case/add/'}),
            'case_name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写接口名称,比如：登录接口测试'}),
            'case_group': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'request_method': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'headers': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写请求头,注意格式：{}'}),
            'params': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写请求参数'}),
            'is_active': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'add_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'update_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'expect_res': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写预期结果断言'}),
            'duration': TextInput(attrs={'class': 'form-control', 'style': 'width:100px;'}),
            'fact_res': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'readonly': True}),
            'request_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'remark': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写备注信息'}),
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
        exclude = ("id", )






















