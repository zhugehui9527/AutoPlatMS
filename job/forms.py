# -*- coding: utf-8 -*-

from __future__ import absolute_import, unicode_literals
from django import forms
from django.forms.widgets import Select
from django.utils.translation import ugettext_lazy as _

from celery import current_app
from celery.utils import cached_property
try:
    from kombu.utils.json import loads
except ImportError:
    from json import loads
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule
# from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
# from django_celery_results.models import TaskResult
from djcelery.models import TaskState as TaskResult

from .models import EmailManager

try:
    from django.utils.encoding import force_text
except ImportError:
    from django.utils.encoding import force_unicode as force_text

class TaskSelectWidget(Select):
    '''任务选择'''
    celery_app = current_app
    _choices = None

    def tasks_as_choices(self):
        _ = self._modules
        tasks = list(sorted(name for name in self.celery_app.tasks if not name.startswith('celery.')))
        # tasks 分组存储为tuple
        return (('', ''), ) + tuple(zip(tasks, tasks))

    @property
    def choices(self):
        if self._choices is None:
            self._choices = self.tasks_as_choices()

        return self._choices

    @choices.setter
    def choices(self, _):
        # ChoiceField.__init__ sets ``self.choices = choices``
        # which would override ours.
        pass

    @cached_property
    def _modules(self):
        self.celery_app.loader.import_default_modules()


class TaskChoiceField(forms.ChoiceField):
    """Field that lets you choose between task names."""
    widget = TaskSelectWidget

    def valid_value(self, value):
        return True


class PeriodicTaskForm(forms.ModelForm):
    """Form that lets you create and modify periodic tasks."""
    def __init__(self, *args, **kwargs):
        super(PeriodicTaskForm, self).__init__(*args, **kwargs)
        self.fields['expires'].label = u'过期时间'
        self.fields['args'].label = u'任务参数'
        self.fields['description'].label = u'描述'
        self.fields['name'].label = u'任务名称'
        self.fields['interval'].label = u'定时间隔'
        self.fields['crontab'].label = u'定时周期'
        self.fields['enabled'].label = u'是否启用'

    regtask = TaskChoiceField(
        label=_('选择模板'),
        required=False,
    )

    task = forms.CharField(
        label=_('模板名称'),
        required=False,
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'})
    )

    kwargs = forms.CharField(
        label=_('任务指令'),
        required=True,
        max_length=200,
        initial='',
        widget=forms.TextInput(attrs={'class': 'form-control',
                                      'style': 'width:450px;',
                                      'placeholder': u'{"group":"your_groupname","name":"scritps_name or command"}',
                                      'value': '{}'}
                               ,)
    )


    class Meta:
        model = PeriodicTask
        exclude = ('id', 'queue', 'exchange', 'routing_key', 'solar')
        ordering = ['-date_changed']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'args': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'interval': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'crontab': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'enabled': forms.Select(choices=((True, u'启用'), (False, u'禁用')),
                                    attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'queue': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'exchange': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'routing_key': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'expires': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                  'placeholder': u'时间格式：2017-01-01 00:00:00'}),
            'last_run_at': forms.DateTimeInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:450px;'}),
        }

    def clean(self):
        data = super(PeriodicTaskForm, self).clean()
        regtask = data.get('regtask')
        if regtask:
            data['task'] = regtask
        if not data['task']:
            exc = forms.ValidationError(_('please input name of task'))
            self._errors['task'] = self.error_class(exc.messages)
            raise exc
        return data

    def _clean_json(self, field):
        value = self.cleaned_data[field]
        try:
            loads(value)
        except ValueError as exc:
            raise forms.ValidationError(_('Unable to parse Json: %s' % exc),)
        return value

    def clean_args(self):
        return self._clean_json('args')

    def clean_kwargs(self):
        return self._clean_json('kwargs')


class IntervalForm(forms.ModelForm):
    '''间隔周期表单'''
    class Meta:
        model = IntervalSchedule
        exclude = ('id', )


class CrontabForm(forms.ModelForm):
    '''周期表单'''
    class Meta:
        model = CrontabSchedule
        exclude = ('id', )


class TaskResultForm(forms.ModelForm):
    '''任务结果表单'''
    class Meta:
        model = TaskResult
        exclude = ('id',)
        # ordering = ['-tstamp']


class EmailMangerForm(forms.ModelForm):
    '''邮件管理表单'''
    class Meta:
        model = EmailManager
        exclude = ('id',)
        widgets = {
            'email_subiect': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'email_message': forms.Textarea(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'email_to': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                               'placeholder': '多个收件人逗号隔开'}),
            'email_cc': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                               'placeholder': '多个收件人逗号隔开'}),
            'email_bcc': forms.TextInput(attrs={'class': 'form-control', 'style': 'width:450px;',
                                                'placeholder': '多个收件人逗号隔开'}),
            'email_enbale': forms.Select(choices=((True, u'启用'), (False, u'禁用')),
                                    attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'eamil_config': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),
            'email_periodictask': forms.Select(attrs={'class': 'form-control', 'style': 'width:450px;'}),

        }


