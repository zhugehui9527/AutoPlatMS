# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals

from celery import shared_task, task
from celery.schedules import crontab
# from AutoPlatMS.celery import app
from subprocess import Popen, PIPE

from django_celery_beat.models import PeriodicTask
from case.api import get_object, api_request
from django.shortcuts import render, HttpResponse
from case.models import CaseGroup, Case, PROTOCOL, REQUEST_TYPE
import datetime
import requests



# @app.task
# def test(arg):
#     print arg



@shared_task
def cmmand(groupid, action):
    gobj = get_object(CaseGroup, id=groupid)
    gname = gobj.name
    cases = Case.objects.filter(case_group__name=gname)
    REQUEST_TYPE_DICT = dict(REQUEST_TYPE)
    if str(action).lower() == 'start' and len(cases):
        for case in cases:
            if case.is_active == 'False':
                print (u'请先启用此接口')
                continue
            case_model = get_object(Case, id=case.id)
            request_type = case_model.request_type
            request_method_int = case_model.request_method
            case_is_active = case_model.is_active
            case_group = CaseGroup.objects.get(name=case_model.case_group)
            path = case_model.path
            protocol = case_model.protocol or case_group.protocol
            print 'protocol: ', protocol
            ip = case_model.ip or case_group.ip
            port = case_model.port or case_group.port

            if protocol == PROTOCOL[2][0]:  # PROTOCOL[2][0] == 2
                url = str(PROTOCOL[2][1]) + '://' + str(ip) + ':' + str(port) + str(path)

            else:
                url = str(PROTOCOL[1][1]) + '://' + str(ip) + ':' + str(port) + str(path)
            # case_is_active == 1 启用 ，2 禁用
            if case_is_active == 1:
                if request_method_int == 2:
                    request_method = 'POST'

                elif request_method_int == 1:
                    request_method = 'GET'

                # 更新content-type
                headers['content-type'] = REQUEST_TYPE_DICT[request_type]

                try:
                    # 合并字典
                    headers = dict(headers, **(eval(case_model.headers)))
                except:
                    headers = headers

                try:
                    params = eval(case_model.params)
                except:
                    params = case_model.params

                try:
                    t1 = datetime.datetime.now()
                    s = requests.session()
                    res = api_request(session=s, method=request_method, url=url, params=params, headers=headers)
                    res_status, res_response_message, res_rheaders, res_relapsed = res
                    # json 数据显示格式化
                    # loads = demjson.decode(res_response_message)
                    # res_response_message = json.dumps(loads, indent=4, sort_keys=False, ensure_ascii=False)
                    case_model.fact_res = res_response_message
                    case_model.duration = res_relapsed
                    case_model.response_code = res_status
                    case_model.response_header = res_rheaders
                    if case_model.expect_res in res_response_message:
                        case_model.status = 2
                    else:
                        case_model.status = 3
                    case_model.save()
                except Exception as e:
                    case_model.status = 4
                    case_model.fact_res = e
                    case_model.duration = datetime.datetime.now() - t1
                    case_model.save()

    else:
        return HttpResponse(u'请检查action 或者 添加接口')



@shared_task
def add(x, y):
    return x + y


@shared_task
def mul(x, y):
    return x * y

@shared_task
def xsum(numbers):
    return sum(numbers)

@shared_task
def send(arg):
   print arg


@shared_task
def func_name():
    print '测试成功'
   


