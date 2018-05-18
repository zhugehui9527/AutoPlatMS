# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .api import MockGroupSerial, MockSerial, mock_one_run
from rest_framework import routers, viewsets, serializers

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from .models import MockGroup,Mock
from django.views.decorators.csrf import csrf_exempt
from accounts.permission import permission_verify
from case.api import get_object
import requests

import sys
# Create your views here.
try:
    import json
except ImportError as e:
    import simplejson as json

class MockViewSet(viewsets.ModelViewSet):
    """
    API端：允许查看和编辑
    """
    queryset = Mock.objects.all()
    serializer_class = MockSerial


class MockGroupViewSet(viewsets.ModelViewSet):
    """
    API端：允许查看和编辑
    """
    queryset = MockGroup.objects.all()
    serializer_class = MockGroupSerial


# from rest_framework import status
# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework.renderers import JSONRenderer
from django.core.serializers.json import DjangoJSONEncoder

from .froms import MockForm, GroupForm



def is_A_in_B(x, y):
    '''
    判断x中所有元素是否都在y中
    :param x: (1, [2,3])
    :param y: [1,2,3]
    :return:
    '''
    for i in x:

        if isinstance(i, list):
            for k in i:
                if k not in y:
                    return False
        elif '}' in i:
            d_dict = eval(str(i))
            for j in d_dict:
                v = d_dict[j]
                if (j not in y) or (v not in y):
                    return False
        else:
            if i not in y:
                return False

    return True



@csrf_exempt
def mock_api(request, path):
    '''拼接mock 地址 并返回 mock 响应'''
    host = request.get_host() # 获取域名

    datas = None
    print('path: %s' % path)
    print('GET:%s' % request.GET)
    print('body:%s' % request.body)
    try:
        m = Mock.objects.get(path__contains=path)
    except Mock.DoesNotExist:
        return

    request_url = 'http://' + host + '/mock/mock_api' + m.path

    is_active = m.is_active
    print('is_active:%s' % is_active)
    if int(is_active) == 2:
        return HttpResponse("此接口被禁用", status=404)

    try:
        m_response = json.loads(m.response)
    except:
        m_response = m.response

    content_type = None

    # 判断路径是否匹配
    if m.headers:
        # ('Content-Type' in m.headers) or ('content-type' in m.headers):
        headers = json.loads(m.headers)
        if ('Content-Type' in m.headers):
            content_type = headers['Content-Type']
        elif ('content-type' in m.headers):
            content_type = headers['content-type']
    # 判断GET请求参数是否匹配
    if request.method == 'GET' and m.request_method == 1:
        datas = request.GET  # 实际请求地址中的参数
        data_list = datas.lists()
        # print('datas:%s' % datas)
        # 请求地址带参数
        if data_list:
            for d_tuple in data_list:
                # print(d_tuple)
                param_contain = m.params or m.path
                # print('m.path:%s' % m.path)
                # 判断请求参数是否匹配
                if is_A_in_B(d_tuple, param_contain):
                    m.mock_path = request_url
                    m.save()
                    if isinstance(m_response, dict):
                        m_response_json = json.dumps(m_response, cls=DjangoJSONEncoder)
                        return HttpResponse(m_response_json, content_type=content_type)
                    else:
                        return HttpResponse(m_response, content_type=content_type)

        else:  # 实际请求地址不带参数
            # request.body 只有post才可以获取参数，GET请求参数要在地址中
            _path_param = None
            # 但是 存储的请求地址中有参数，则把参数分片获取
            if '?' in m.path:
                _path_param = m.path.split('?')[-1]

            # 如果配置参数为空 并且 请求地址获取参数也为空
            if (not m.params) and (not _path_param):
                m.mock_path = request_url
                m.save()
                if isinstance(m_response, dict):
                    m_response_json = json.dumps(m_response, cls=DjangoJSONEncoder)
                    return HttpResponse(m_response_json, content_type=content_type)
                else:
                    return HttpResponse(m_response, content_type=content_type)
    elif request.method == 'POST' and m.request_method == 2:
        datas = str(request.body, encoding='utf-8')
        params_str = m.params
        try:
            datas_dict = json.loads(datas)
            params_dict = json.loads(m.params)
            if isinstance(datas_dict, dict) and isinstance(params_dict, dict):
                if datas_dict == params_dict:
                    print('datas == params_dict')
                    m.mock_path = request_url
                    m.save()
                    if isinstance(m_response, dict):
                        m_response_json = json.dumps(m_response, cls=DjangoJSONEncoder)
                        return HttpResponse(m_response_json, content_type=content_type)
                    else:
                        return HttpResponse(m_response, content_type=content_type)

        except:
            if params_str == datas:
                m.mock_path = request_url
                m.save()
                if isinstance(m_response, dict):
                    m_response_json = json.dumps(m_response, cls=DjangoJSONEncoder)
                    return HttpResponse(m_response_json, content_type=content_type)
                else:
                    return HttpResponse(m_response, content_type=content_type)

    error_msg = {
             "errcode": 404,
             "errmsg": "This API does not exist, current path is: {},method is: {} , please confirm your request config!".format(
             request.path_info, request.method),
             "data": datas
             }
    print(error_msg)
    error_msg_json = json.dumps(error_msg, cls=DjangoJSONEncoder)
    return HttpResponse(error_msg_json, status=404)



# @api_view(['GET', 'POST'])
# @csrf_exempt
# @permission_verify
def mock_index(request):
    '''获取所有mock接口列表'''
    temp_name = "mock/mock-header.html"
    mock_list = Mock.objects.all()

    user = request.user
    return render(request, 'mock/index.html', locals())

# 希望post能够不通过CSRF token的验证，所以我们使用了 csrf_exempt
# @csrf_exempt
@permission_verify()
def mock_add(request):
    '''获取所有mock接口列表'''
    temp_name = "mock/mock-header.html"

    if request.method == 'POST':
        mock_form = MockForm(request.POST)

        # c_form.is_valid() 用户输入是否合法
        if mock_form.is_valid():
            mock_form.save()
            tips = u'增加成功！'
            display_control = ''
        else:
            tips = u'增加失败！'
            display_control = ''
        return render(request, 'mock/mock_add.html', locals())
    else:
        display_control = 'none'
        tips = ''
        mock_form = MockForm()
        return render(request, 'mock/mock_add.html', locals())


# @csrf_exempt
# @api_view(['GET', 'POST'])
@permission_verify()
def mock_edit(request, ids):
    '''获取所有mock接口列表'''
    temp_name = "mock/mock-header.html"
    obj = get_object(Mock, id=ids)
    mod_status = 0
    if request.method.lower() == 'post':
        cf = MockForm(request.POST, instance=obj)

        if cf.is_valid():
            # response = str(cf.response)

            cf.save()
            mod_status = 1
        else:
            mod_status = 2

    else:
        cf = MockForm(instance=obj)
    return render(request, 'mock/mock_edit.html', locals())


# @csrf_exempt
# @api_view(['GET', 'POST'])
@permission_verify()
def mock_del(request):
    '''获取所有mock接口列表'''
    temp_name = "mock/mock-header.html"
    # mock_list = Mock.objects.all()
    case_id = request.GET.get('id', '')
    # 直接删除
    if case_id:
        Mock.objects.get(id=case_id).delete()

    # 删除勾选用例
    if request.method.lower() == 'post':
        case_batch = request.GET.get('arg', '')
        mock_id_all = str(request.POST.get('mock_id_all', ''))
        if case_batch:
            for case_id in mock_id_all.split(','):
                case_item = get_object(Mock, id=case_id)
                case_item.delete()
    return redirect('/mock/index/')



# def mock_info(request, ids):
#     '''查看mock 接口信息'''
#     temp_name = "mock/mock-header.html"
#     obj = get_object(Mock, id=ids)
#
#     return render(request, 'mock/mock_info.html', locals())


# @csrf_exempt
# @api_view(['GET', 'POST'])
def mock_run(request, ids):
    '''获取所有mock接口列表'''
    temp_name = "mock/mock-header.html"
    m = get_object(Mock, id=ids)
    _path = m.path
    param = m.params
    try:
        param = json.loads(param)
    except:
        pass
    host = request.get_host()
    url = 'http://' + host + '/mock/mock_api' + _path
    method = m.request_method
    res = None
    headers = None
    if m.headers:
        headers = json.loads(m.headers)

    if method == 1:
        res = requests.get(url=url, params=param, headers=headers)
    elif method == 2:
        if isinstance(param, dict):
            res = requests.post(url=url, json=param, headers=headers)
        else:
            res = requests.post(url=url, data=param, headers=headers)

    response_code = 500
    response_msg = None
    response_headers = None
    if res:
        response_code = res.status_code
        try:
            response_msg = res.json()
        except:
            response_msg = res.text
        response_headers = res.headers

    return render(request, 'mock/mock_info.html', locals())


# @csrf_exempt
# @api_view(['GET', 'POST'])
@permission_verify()
def group(request):
    temp_name = "mock/mock-header.html"
    allgroup = MockGroup.objects.all()
    return render(request, 'mock/group_index.html', locals())


# @api_view(['GET', 'POST'])
@permission_verify()
def group_add(request):
    '''添加属组'''
    temp_name = 'mock/mock-header.html'
    if request.method == 'POST':
        # GroupForm(request.POST) 接收POST表单数据
        group_form = GroupForm(request.POST)
        if group_form.is_valid():
            group_form.save()
            tips = u'增加成功！'
            display_control = ''
        else:
            tips = u'增加失败！'
            display_control = ''
        return render(request, 'mock/group_add.html', locals())
    else:
        display_control = "none"
        group_form = GroupForm()
        return render(request, 'mock/group_add.html', locals())

@permission_verify()
def group_edit(request, ids):
    '''编辑mock属组'''
    obj = get_object(MockGroup, id=ids)
    allgroup = MockGroup.objects.all()
    unselect = Mock.objects.filter(group__name=None)
    members = Mock.objects.filter(group__name=obj.name)
    mod_status = 0
    if request.method == 'POST':
        group_form = GroupForm(request.POST, instance=obj)
        if group_form.is_valid():
            group_form.save()
            mod_status = 1
        else:
            mod_status = 2
    else:
        group_form = GroupForm(instance=obj)
    return render(request, 'mock/group_edit.html', locals())

@permission_verify()
def group_del(request):
    '''案例集删除'''
    temp_name = 'mock/mock-header.html'
    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        group_id = request.POST.get("id", "")
        if group_id:
            MockGroup.objects.get(id=group_id).delete()
        if group_items:
            for n in group_items:
                MockGroup.objects.filter(id=n).delete()
    allgroup = MockGroup.objects.all()
    return render(request, 'mock/group_index.html', locals())

@permission_verify()
def group_save(request):
    '''案例集保存'''
    temp_name = 'mock/mock-header.html'
    mod_status = 0
    if request.method == 'POST':
        group_id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        members = request.POST.getlist('members', [])
        unselect = request.POST.getlist('unselect', [])
        group_item = MockGroup.objects.get(id=group_id)
        if unselect:
            for mock in unselect:
                obj = Mock.objects.get(name=mock)
                obj.group_id = None
                obj.save()
        if members:
            for mock in members:
                obj = Mock.objects.get(name=mock)
                obj.group_id = group_id
                obj.save()
        group_item.name = name
        group_item.desc = desc
        group_item.save()
        obj = group_item
        mod_status = 1
    else:
        mod_status = 2

    return render(request, 'mock/group_edit.html', locals())
