# -*- coding:utf-8 -*-
from django import forms
from django.forms.widgets import *
from .models import Mock, MockGroup

class MockForm(forms.ModelForm):
    '''接口表单'''
    class Meta:
        ''' 模型表单 '''
        model = Mock
        # exclude 除了这些不用渲染
        exclude = ("id", "create_time", "update_time", "status", "duration", "mock_path" )
        # widgets 用来渲染成HTML元素的工具
        widgets = {
            'path': TextInput(
                attrs={'class': 'form-control', 'style': 'width:530px',
                       'placeholder': u'请填写接口请求路径,比如: /casemanage/case/add/'}),
            'name': TextInput(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写接口名称,比如：登录接口测试'}),
            'group': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'request_method': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'headers': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写请求头,注意格式：{}'}),
            'params': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写请求参数'}),
            'is_active': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'create_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'update_time': DateTimeInput(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            # 'duration': TextInput(attrs={'class': 'form-control', 'style': 'width:100px;'}),
            'response': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'request_type': Select(attrs={'class': 'form-control', 'style': 'width:530px;'}),
            'remark': Textarea(attrs={'class': 'form-control', 'style': 'width:530px;', 'placeholder': u'请填写备注信息'}),
        }


class GroupForm(forms.ModelForm):
    '''mock 组表单'''
    def clean(self):
        cleaned_data = super(GroupForm, self).clean()
        value = cleaned_data.get('name')
        try:
            MockGroup.objects.get(name=value)
            self._errors['name'] = self.error_class(['%s 的信息已经存在' % value])
        except MockGroup.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = MockGroup
        exclude = ("id", "create_time", "update_time")
        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control', 'style': 'width:480px',
                       'placeholder': u'请填写组名'}),
            'desc': TextInput(
                attrs={'class': 'form-control', 'style': 'width:480px',
                       'placeholder': u'请填写描述'}),
            # 'protocol': Select(attrs={'class': 'form-control', 'style': 'width:480px;'}),
            # 'ip': TextInput(
            #     attrs={'class': 'form-control', 'style': 'width:480px;', 'placeholder': u'请填写域名或者ip'}),
            # 'port': TextInput(
            #     attrs={'class': 'form-control', 'style': 'width:480px;', 'placeholder': u'请填写端口'}),
        }






















