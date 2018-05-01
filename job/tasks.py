# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import shared_task, Task
from AutoPlatMS.celery_init import app
from .api import send_mail
from django.core import mail
# from djcelery_email.tasks import send_email
from django.template import loader, Context
# from case.api import get_object, api_request
# from django.shortcuts import render, HttpResponse
# from case.models import CaseGroup, Case, PROTOCOL, REQUEST_TYPE
# import datetime
# import requests
import logging
logger = logging.getLogger(__name__)


class MyTask(Task):
    '''任务回调函数'''
    def on_success(self, retval, task_id, args, kwargs):
        '''
        :param retval:  任务返回值
        :param task_id:  任务task_id
        :param args: 任务参数
        :param kwargs: 任务参数名
        :return: The return value of this handler is ignored.
        '''
        print('task success: {0}, task_id:{1},args:{2} '.format(retval, task_id, args))
        # super(MyTask, self).update_state(task_id=task_id, state='SUCCESS')
        # super(MyTask, self).on_success(retval, task_id, args, kwargs)
        # import time
        # time.sleep(5)
        # from .api import send_task_mail
        # send_task_mail(task_id)
        # print('发送邮件完成')
        return super(MyTask, self).on_success(retval, task_id, args, kwargs)


    def on_failure(self, exc, task_id, args, kwargs, einfo):
        '''
        :param exc: 任务失败抛出的异常
        :param task_id: 任务task_id
        :param args: 任务参数
        :param kwargs: 任务参数名
        :param einfo:  ExceptionInfo instance, containing the traceback.
        :return: The return value of this handler is ignored.
        '''
        print('task fail, reason: {0},task_id:{1},args:{2}, kwargs:{3},  einfo:{4}'.format(exc, task_id, args, kwargs, einfo))
        import time
        time.sleep(3)
        from .api import send_task_mail
        send_task_mail(task_id)
        return super(MyTask, self).on_failure(exc, task_id, args, kwargs, einfo)

    def send_error_email(self, context, exc, **kwargs):
        print('context: {0}, exc:{1}'.format(context, exc))

        return super(MyTask, self).send_error_email(context, exc, **kwargs)

    def after_return(self, status, retval, task_id, args, kwargs, einfo):
        '''

        :param status:
        :param retval:
        :param task_id:
        :param args:
        :param kwargs:
        :param einfo:
        :return:
        '''
        print('after_return, status: {0},task_id:{1},args:{2}, kwargs:{3},  einfo:{4}, id:{5}'.format(status,
         task_id, args, kwargs, einfo, self.request.id))
        import time
        time.sleep(3)
        from .api import send_task_mail
        send_task_mail(task_id)
        return super(MyTask, self).after_return(status, retval, task_id, args, kwargs, einfo)


@app.task
def test():
    print("test ....")


@shared_task(base=MyTask)
def runCaseGroup(*args):
    '''
    运行接口任务
    :param args: 用例集合名称
    :return:
    '''
    from case.api import run_group_name
    if isinstance(args, tuple) or isinstance(args, list):
        for arg in args:
            run_group_name(arg)
        return '%s run finished' % args


@shared_task(base=MyTask)
def add(x, y):
    z = x + y
    return z

@shared_task(base=MyTask)
def mul(x, y):
    return x * y

@shared_task(base=MyTask)
def xsum(numbers):
    return sum(numbers)

@shared_task(base=MyTask)
def send_msg(arg):
   return arg


@shared_task(base=MyTask)
def func_name():
    print('测试成功')


@shared_task(base=MyTask)
def hostname():
    import subprocess
    return subprocess.check_output(['hostname'])


@shared_task(base=MyTask)
def sendmail(subject, message, from_email, recipient_list, to_cc=None, to_bcc=None, **kwrags):
    '''
    发送邮件
    :param subject:
    :param message:
    :param from_email:
    :param recipient_list:
    :param to_cc:
    :param to_bcc:
    :param kwrags:
    :return:
    '''
    try:
        # 使用celery并发处理邮件发送的任务
        logger.info("\n开始发送邮件")
        # 方法1
        # mail.send_mail(subject, message, from_email, [recipient_list], **kwrags)
        # 方法2 发送html邮件

        send_mail(subject, message, from_email, recipient_list, to_cc=None, to_bcc=None, **kwrags)
        logger.info("邮件发送成功")
        return 'send mail success!'
    except Exception as e:
        logger.error("邮件发送失败: {}".format(e))
        raise e


