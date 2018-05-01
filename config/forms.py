# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from django import forms
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _

from .models import EmailConfig


class EmailConfigForm(forms.ModelForm):
    '''邮件管理表单'''
    def clean(self):

        cleaned_data = super(EmailConfigForm, self).clean()
        value = cleaned_data.get('email_user')
        try:
            EmailConfig.objects.get(email_user=value)
            self._errors['email_user'] = self.error_class(['%s 的信息已经存在' % value])
        except EmailConfig.DoesNotExist:
            pass
        return cleaned_data

    class Meta:
        model = EmailConfig
        exclude = ('id',)
        widgets = {
            u'邮箱账号': forms.EmailInput(attrs={'class': 'form-control', 'style': 'width:450px;',}),
            u'邮箱密码': forms.PasswordInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            u'邮箱域名': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;',}),
            u'邮箱端口': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;', }),
        }