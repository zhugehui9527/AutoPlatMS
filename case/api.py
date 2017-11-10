# -*- coding:utf-8 -*-
from django.http import HttpResponse
from models import Case, CaseGroup
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.csrf import csrf_exempt
from lib.common import token_verify
import requests

try:
    import json
except ImportError, e:
    import simplejson as json


def str2gb(args):
    '''
    :param args:
    :return: gb2312
    '''
    return str(args).encode('gb2312')


def get_object(model, **kwargs):
    '''
    查询数据库
    :param model:
    :param kwargs:
    :return:
    '''
    for value in kwargs.values():
        if not value:
            return None
    the_object = model.objects.filter(**kwargs)
    if len(the_object) == 1:
        the_object = the_object[0]
    else:
        the_object = None
    return the_object

def page_list_return(total, current=1):
    '''
    page 分页，返回本次分页的最小和最大页数列表
    :param total:
    :param current:
    :return:
    '''
    min_page = current - 2 if current -4 > 0 else 1
    max_page = min_page + 4 if min_page + 4 < total else total
    return range(min_page, max_page+1)


def pages(post_objects, request):
    """
        page public function , return page's object tuple
        分页公用函数，返回分页的对象元组
        """
    paginator = Paginator(post_objects, 65535)
    try:
        current_page = int(request.GET.get('page', '1'))
    except ValueError:
        current_page = 1

    page_range = page_list_return(len(paginator.page_range), current_page)

    try:
        page_objects = paginator.page(current_page)
    except (EmptyPage, InvalidPage):
        page_objects = paginator.page(paginator.num_pages)

    if current_page >= 5:
        show_first = 1
    else:
        show_first = 0

    if current_page <= (len(paginator.page_range) - 3):
        show_end = 1
    else:
        show_end = 0

    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    return post_objects, paginator, page_objects, page_range, current_page, show_first, show_end


@csrf_exempt
@token_verify()
def collect(request):
    case_info = json.loads(request.body)
    if request.method == 'POST':
        url = case_info['url']
        case_name = case_info['case_name']
        # case_group = case_info['case_group']
        request_method = ''
        headers = case_info['headers']
        params = case_info['params']
        is_active = ''
        add_time = case_info['add_time']
        update_time = case_info['update_time']
        expect_res = case_info['expect_res']
        fact_res = case_info['fact_res']
        try:
            case = Case.objects.get(case_name=case_name)
        except:
            case = Case()

        case.case_name = case_name
        case.add_time = add_time
        case.request_method = request_method
        case.params = params
        case.headers = headers
        case.is_active = is_active
        case.update_time = update_time
        case.expect_res = expect_res
        case.fact_res = fact_res
        case.url = url
        case.save()
        return HttpResponse('Post case data to server success!')

    else:
        return HttpResponse('No any data to post')


@token_verify()
def get_case(request):
    try:
        case_name = request.GET('name')
    except:
        return HttpResponse('You have no data !')

    try:
        case = Case.objects.get(case_name=case_name)
    except:
        return HttpResponse('no data, please check your case')

    data = {'case_name': case.case_name,
            'url': case.url,
            'request_method': case.request_method,
            'params': case.params,
            'headers': case.headers,
            'is_active': case.is_active,
            'update_time': case.update_time,
            'expect_res': case.expect_res,
            'fact_res': case.fact_res,
            'duration': case.duration,
            'status': case.status,
            'case_group': case.case_group,

            }
    return HttpResponse(json.dumps({'status': 0, 'message': 'OK','data': data}))


@token_verify()
def get_group(request):
    if request.GET:
        d = []
        try:
            group_name = request.GET['name']
        except:
            return HttpResponse('your parameter is error')
        if group_name == 'all':
            case_groups = CaseGroup.objects.all()
            for cg in case_groups:
                ret_cg = {'case_group': cg.name, 'memebers':[]}
                memebers = Case.objects.filter(case_group=cg)
                for c in memebers:
                    ret_c = {'case_name': c.case_name, }
                    ret_cg['members'].append(ret_c)
                d.append(ret_cg)
            return HttpResponse(json.dumps(d))

        else:
            ret_cg = {'case_group': group_name, 'memebers':[]}
            memebers = Case.objects.filter(group_name=group_name)
            for c in memebers:
                ret_c = {'case_name': c.case_name, }
                ret_cg['memebers'].append(ret_c)
            d.append(ret_cg)
            return HttpResponse(json.dumps(d))
    return HttpResponse(status=403)


def api_request( method, url, **kwargs):
    '''http 接口请求'''
    r = requests.request(method, url, **kwargs)
    status_code = r.status_code
    response_message = r.content
    rheaders = r.headers
    relapsed = r.elapsed
    return status_code, response_message, rheaders, relapsed









