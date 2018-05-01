# -*- coding:utf-8 -*-
from django.http import HttpResponse
# from django.views.decorators.csrf import csrf_exempt
# from lib.common import token_verify
from djcelery.models import TaskState, PeriodicTask

from django.core.serializers.json import DjangoJSONEncoder
import pytz
try:
    import json
except ImportError as e:
    import simplejson as json


import logging
logger = logging.getLogger('django')

def get_job_state(request):
    '''
    根据任务结果和job列表中taskname，关联获取任务state
    :param request:
    :return:
    '''
    job_name = request.GET['name']
    get_job_obj = PeriodicTask.objects.get(name=job_name)
    # 新建job 查询结果优化
    get_task_name = get_job_obj.task
    last_run_at = get_job_obj.last_run_at
    arg = eval(get_job_obj.args)
    kwargs = eval(get_job_obj.kwargs)

    if get_task_name:
        try:
            taskstate = TaskState.objects.filter(name=get_task_name)
            task_info = taskstate.filter(tstamp__gt=last_run_at).filter(args=str(arg)).filter(kwargs=str(kwargs)).\
                values_list('name', 'state', 'tstamp').first()
            tstamp = task_info[2]

            # 设置时区
            tz = pytz.timezone('Asia/Shanghai')
            # 时区转换，原来的时区是UTC
            tstamps = tstamp.astimezone(tz)
            # import time
            # tstamps = time.strftime('%Y-%m-%d %H:%M:%S',tstamps )
            ss = {'code': 0, 'taskname': task_info[0], 'taskstate': task_info[1], 'tstamp': tstamps}

            json_ss = json.dumps(ss, cls=DjangoJSONEncoder)
            return HttpResponse(json_ss)
        except TaskState.DoesNotExist:
            ss = {'code': 1, 'taskstate': 'None'}
            json_ss = json.dumps(ss, cls=DjangoJSONEncoder)
            return HttpResponse(json_ss)
        except Exception:
            ss = {'code': 1, 'taskstate': 'None'}
            json_ss = json.dumps(ss, cls=DjangoJSONEncoder)
            return HttpResponse(json_ss)
    else:
        res2 = {'code': 2, 'msg': 'Not find this task!'}
        return HttpResponse(json.dumps(res2, cls=DjangoJSONEncoder))


def run_job_case_group(request, ids):
    '''运行某一个job'''
    from job import tasks
    # job_id = request.GET('ids')
    if request.method == 'GET':
        periodtask = PeriodicTask.objects.get(id=ids)
        args = eval(periodtask.args)
        kwargs = eval(periodtask.kwargs)

        ret = None
        if isinstance(args, list) and args:
            ret = tasks.runCaseGroup.delay(args)
        elif isinstance(kwargs, dict) and kwargs:
            groups = []
            for value in kwargs:
                groups.append(kwargs[value])
            ret = tasks.runCaseGroup.delay(groups)

        return HttpResponse(ret.get())


from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from case.models import Case
import datetime
import sys, os
import django
import celery


@csrf_exempt
def get_latest_report(request, ids):
    '''
    任务列表获取某一个任务的最新报告
    :param request:
    :param ids: 任务id
    :return:
    '''
    java_home = os.popen('echo $JAVA_HOME').read()
    python_version = str(sys.version).split(' ')[0]
    platform = sys.platform
    generate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    django_version = django.get_version()
    celery_version = celery.VERSION_BANNER

    get_job_name = None
    state = None
    tstamp = None
    runtime = None
    build_id = None
    groupname = None
    # build info
    from job.models import PeriodicTask, TaskState
    periodic = PeriodicTask.objects.get(id=ids)
    get_job_name = periodic.name
    name = periodic.task
    args = eval(periodic.args)
    kwargs = eval(periodic.kwargs)
    last_run_at = periodic.last_run_at
    try:
        taskstate = TaskState.objects.filter(name=name).filter(tstamp__gt=last_run_at).filter(args=str(args)).\
            filter(kwargs=str(kwargs)).values_list('name', 'state', 'tstamp', 'runtime', 'id').first()
        state = taskstate[1]
        tstamp = taskstate[2]
        runtime = taskstate[3]
        build_id = taskstate[4]
    except:
        return HttpResponse('%s matching query does not exist' % get_job_name)

    groupname = args[0]
    from case.models import GroupResult
    group_result = GroupResult.objects.get(group__name=groupname)
    summary = {
        'res_count': group_result.res_count,
        'res_status': group_result.res_status,
        'res_success': group_result.res_success,
        'res_fail': group_result.res_fail,
        'res_error': group_result.res_error,
        'res_duration': group_result.res_duration,
        'res_rerun': group_result.res_rerun
    }
    cases = Case.objects.filter(case_group__name=groupname)

    return render(request, 'latest_report.html', locals())

@csrf_exempt
def show_result_report(request, ids):
    '''
    显示构建任务结果报告
    :param request:
    :param ids: 构建任务结果ID
    :return:
    '''
    build_id = ids
    # environment info
    java_home = os.popen('echo $JAVA_HOME').read()
    python_version = str(sys.version).split(' ')[0]
    platform = sys.platform
    generate_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    django_version = django.get_version()
    celery_version = celery.VERSION_BANNER
    cases = None
    summary = None
    get_job_name = None
    # build info
    from job.models import PeriodicTask, TaskState
    taskstate = TaskState.objects.get(id=build_id)
    runtime = taskstate.runtime
    result = taskstate.result
    state = taskstate.state
    args = taskstate.args
    kwargs = taskstate.kwargs
    tstamp = taskstate.tstamp
    name = taskstate.name

    if name == 'job.tasks.runCaseGroup':
        args = eval(args)
        job_objs = PeriodicTask.objects.filter(task=name)
        job_obj = None
        for i, job in enumerate(job_objs):
            args_ = eval(job.args)
            if args == args_:
                job_obj = job_objs[i]
                break

        get_job_name = job_obj.name
        last_run_at = job_obj.last_run_at
        groupname = args[0]

        from case.models import GroupResult
        group_result = GroupResult.objects.get(group__name=groupname)
        summary = {
            'res_count': group_result.res_count,
            'res_status': group_result.res_status,
            'res_success': group_result.res_success,
            'res_fail': group_result.res_fail,
            'res_error': group_result.res_error,
            'res_duration': group_result.res_duration,
            'res_rerun': group_result.res_rerun
        }
        cases = Case.objects.filter(case_group__name=groupname)

    return render(request, 'latest_report.html', locals())


from django.core import mail
from django.template import loader


def send_mail(subject, message, from_email, recipient_list, to_cc=None, to_bcc=None, **kwrags):
    '''settings : 配置发送邮件'''
    context = {
        'title': subject,
        'content_text': message,
    }
    email_template_name = 'template_report.html'
    t = loader.get_template(email_template_name)
    # c = Context(context)
    html_content = t.render(context)
    # mail.send_mail(subject, message, from_email, [recipient_list], **kwrags)
    recipient_list = str(recipient_list).split(',')
    to_cc = str(to_cc).split(',')
    to_bcc = str(to_bcc).split(',')
    logger.info("recipient_list: %s" % recipient_list)
    msg = mail.EmailMultiAlternatives(subject=subject, body=html_content, from_email=from_email,
                                      to=recipient_list, cc=to_cc, bcc=to_bcc, **kwrags)
    msg.attach_alternative(html_content, 'text/html')
    # msg.attach_file(u'D:/My Documents/Python/doc/test.doc')  # 添加附件发送
    msg.send()

def sendmail(from_, pwd, host, port, subject, body, recipient_list, type='html', attachfile=None):
    '''封装发送邮件接口'''
    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.utils import formataddr

    msg = MIMEMultipart()
    msg['From'] = formataddr(["ATMS", from_])
    for to_ in recipient_list:
        msg['To'] = formataddr([to_, to_])
    msg['Subject'] = subject
    msg_ = MIMEText(body, type, 'utf-8')
    msg.attach(msg_)
    if attachfile:
        att = MIMEText(body, 'base64', 'utf-8')
        att["Content-Type"] = "application/octet-stream"
        att["Content-Disposition"] = 'attachment; filename="{}"'.format(attachfile)
        msg.attach(att)
    try:

        server = smtplib.SMTP_SSL(host, port)  # 发件人邮箱中的SMTP服务器，端口是25
        server.login(from_, pwd)  # 括号中对应的是发件人邮箱账号、邮箱密码
        server.sendmail(from_, recipient_list, msg.as_string())  # 括号中对应的是发件人邮箱账号、收件人邮箱账号、发送邮件
        server.quit()  # 关闭连接
        print("邮件发送成功")

    except smtplib.SMTPException:
        print("Error: 无法发送邮件")


@csrf_exempt
def get_task_state(request, udid):
    from djcelery.models import TaskState
    if request.method == 'GET':
        try:
            taskstate = TaskState.objects.get(task_id=udid)
            name = taskstate.name
            id_ = taskstate.id
            state = taskstate.state
            args = taskstate.args
            kwargs = taskstate.kwargs
        except TaskState.DoesNotExist:
            name = ''
            id_ = ''
            state = ''
            args = []
            kwargs = {}
        task = {
            'name': name,
            'task_id': udid,
            'state': state,
            'id': id_,
            'kwargs': kwargs,
            'args': args,
        }
        msg_json = json.dumps(task, cls=DjangoJSONEncoder)

        return HttpResponse(msg_json)


def send_task_mail(task_id):
    '''
    调用数据库配置发送邮件
    :param task_id: 任务结果id
    :return:
    '''

    import requests
    state_ = requests.get('http://127.0.0.1:8000/jobs/job/getstate/{}/'.format(task_id))
    state_json = state_.json()
    print(state_json)
    if isinstance(state_json, dict):

        state_json_a = state_json
        name = state_json_a['name']
        buildid = state_json_a['id']
        state = state_json_a['state']
        args = state_json_a['args']

        if name != 'job.tasks.runCaseGroup':
            return False

        req = requests.get('http://127.0.0.1:8000/jobs/job/report/{}/'.format(buildid))
        # req = requests.get('http://127.0.0.1:8000/jobs/job/latest/{}/'.format(buildid))
        res = req.text
        report_path = './report/report.html'

        with open(report_path, 'w+') as f:
            f.write(res)
            f.close()
        # from config.models import EmailConfig
        # try:
        #     email_config = EmailConfig.objects.filter(emailmanager__email_periodictask__task=name).filter(
        #         emailmanager__email_periodictask__args=eval(args)).get()
        #
        # except Exception as e:
        #     raise e
        # logger.info(email_config)

        from job.models import EmailManager
        try:
            email_manager = EmailManager.objects.filter(email_periodictask__task=name).get(email_periodictask__args=args.replace('\'', '"'))
            enbale = email_manager.email_enbale
            # print('enable: %s' % type(enbale))
            if str(enbale) == 'False':
                return False
            to_ = str(email_manager.email_to).split(',')
            from_ = email_manager.eamil_config.email_user
            logger.info('from_:%s' % from_)
            pwd = email_manager.eamil_config.email_pwd
            host = email_manager.eamil_config.email_host
            port = email_manager.eamil_config.email_port

            subject = email_manager.email_subiect or "Task:%s, ID: %s, STATE:%s" % (name, buildid, state)
            body = email_manager.email_message or res
            logger.info('subject:%s ' % subject)
            logger.info('body:%s ' % body)
            sendmail(from_=from_, pwd=pwd, host=host, port=port,
                     subject=subject, body=body, recipient_list=to_, attachfile='report.html')
        except Exception as e:
            raise e




