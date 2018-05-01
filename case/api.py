# -*- coding:utf-8 -*-
from django.http import HttpResponse
from .models import Case, CaseGroup, PROTOCOL, REQUEST_TYPE
from django.core.paginator import Paginator, EmptyPage, InvalidPage
from django.views.decorators.csrf import csrf_exempt
from lib.common import token_verify
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import datetime, requests
from django.core.serializers.json import DjangoJSONEncoder

try:
    import json
except ImportError as e:
    import simplejson as json

def getSecond(time):
    '''
    :param time: 0:00:00.023274
    :return: 秒的字符串
    '''
    times = str(time).split('.')
    time_ms = times[-1]
    time_p = times[0].split(':')
    time_h = time_p[0]
    time_m = time_p[1]
    time_s = time_p[2]
    time_f = str(int(time_h) * 3600 + int(time_m) * 60 + int(time_s)) + '.' + str(time_ms)
    return time_f

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


@login_required()
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
            memebers = Case.objects.filter(case_group__name=group_name)
            for c in memebers:
                ret_c = {'case_name': c.case_name, }
                ret_cg['memebers'].append(ret_c)
            d.append(ret_cg)
            return HttpResponse(json.dumps(d))
    return HttpResponse(status=403)


def api_request(session, method, url, **kwargs):
    '''http 接口请求'''
    if method.lower() == 'post':
        r = session.post(url, **kwargs)
    else:
        r = session.get(url, **kwargs)
    status_code = r.status_code
    response_message = r.content
    rheaders = r.headers
    relapsed = r.elapsed
    return status_code, response_message, rheaders, relapsed


@login_required()
@permission_verify()
def update_index(request):
    """ 更新接口的索引"""
    # print "ready request index1"
    if request.method.lower() == 'post':

        try:
            # print "ready request index2"
            index = request.GET.get('index', '')
            # print "ready request index: %s" % index
            case_id = request.POST.get('id', '')
            # print "ready request id: %s " % case_id

        except:
            return HttpResponse('You have no data !')

        try:

            case = Case.objects.get(id=case_id)

            case.NO = int(index)
            case.save()
            # print "request index success"
        except:
            return HttpResponse('no data, please check your case')

        data = {'NO': index,
                'id': case.id,
                'name': case.case_name,

                }
        res_dict = {'status': 0, 'message': 'OK', 'data': data}
        json_ss = json.dumps(res_dict, cls=DjangoJSONEncoder)
        return HttpResponse(json_ss)


@login_required()
@permission_verify()
def get_case_list(request):
    if request.method.lower == 'get':
        try:
            case = Case.objects.all()

        except:
            return HttpResponse('no data, please check your cases')


def run_one_case(case_id):
    '''
    运行单个接口
    :param case_id:
    :return:
    '''
    headers = {}
    proxies = {"http": None, "https": None}
    REQUEST_TYPE_DICT = dict(REQUEST_TYPE)
    request_method = 'GET'
    if case_id:
        case_model = Case.objects.get(id=case_id)
        group_name = case_model.case_group.name
        case_is_active = case_model.is_active
        case_group = CaseGroup.objects.get(name=group_name)
        path = case_model.path

        protocol = case_model.protocol or case_group.protocol
        ip = case_model.ip or case_group.ip

        if protocol == PROTOCOL[2][0]:  # PROTOCOL[2][0] == 2
            port = case_model.port or case_group.port or 443
            url = str(PROTOCOL[2][1]) + '://' + str(ip) + ':' + str(port) + str(path)

        else:
            port = case_model.port or case_group.port or 80
            url = str(PROTOCOL[1][1]) + '://' + str(ip) + ':' + str(port) + str(path)

        # content_type = case_model.content_type
        # case_is_active == 1 启用 ，2 禁用
        if case_is_active == 1:
            request_method_int = case_model.request_method
            if request_method_int == 2:
                request_method = 'POST'

            request_type = case_model.request_type
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
                case_proxies = case_model.proxies
                group_proxies = case_group.proxies
                if group_proxies:
                    proxies["http"] = group_proxies
                    proxies["https"] = group_proxies

                if case_proxies:
                    proxies["http"] = case_proxies
                    proxies["https"] = case_proxies

            except:
                proxies = {}

            t1 = datetime.datetime.now()
            res_status = 500
            try:
                s = requests.session()
                res = api_request(session=s, method=request_method, url=url, params=params, headers=headers,
                                  proxies=proxies)
                res_status, res_response_message, res_rheaders, res_relapsed = res
                case_model.headers = headers
                case_model.duration = getSecond(res_relapsed)
                case_model.response_code = res_status
                case_model.response_header = res_rheaders
                _expect_res = case_model.expect_res

                res_response_json = str(res_response_message, encoding='utf-8')
                # print('res_response_json：%s' % res_response_json)

                # if isinstance(_expect_res, bytes) or isinstance(_expect_res, str) :
                #     # 去掉字符串中的空格
                #     _expect_res = str(_expect_res).replace(' ', '')
                # 去除期望结果中的空字符以及实际响应中的空字符，并判断
                try:
                    # 如果是json格式数据，则转化为dict，并排序
                    _expect_res = sorted(json.loads(_expect_res))
                    res_response_message = sorted(json.loads(res_response_json))
                except:
                    pass

                if isinstance(_expect_res, dict):
                    if _expect_res == res_response_message or (not _expect_res):
                        case_model.traceback = None
                        case_model.status = 2
                    else:
                        case_model.status = 3
                        case_model.traceback = u'断言失败，预期结果：%s' % _expect_res
                elif isinstance(_expect_res, str):

                    if isinstance(res_response_message, dict):
                        res_response_json = str(json.loads(res_response_json))
                    # print('_expect_res:%s' % _expect_res)
                    if (_expect_res == res_response_json) or (_expect_res in res_response_json) or (not _expect_res):
                        case_model.traceback = None
                        case_model.status = 2
                    else:
                        case_model.status = 3
                        case_model.traceback = u'断言失败，预期结果：%s' % _expect_res

                case_model.fact_res = res_response_json
                case_model.save()
            except Exception as e:
                case_model.status = 4
                case_model.fact_res = e
                case_model.traceback = e
                case_model.response_code = res_status
                case_model.duration = datetime.datetime.now() - t1
                case_model.save()


def run_all_case(case_id_all):
    '''
    运行所有接口
    :param case_id_all: 接口id
    :return:
    '''
    for case_id in case_id_all:
        run_one_case(case_id)


def run_group_name(groupname):
    '''
    运行一个用例集合
    :param groupid:
    :return:
    '''
    # cases = Case.objects.filter(case_group__name=groupname)
    # if len(cases):
    #     for case in cases:
    #         run_one_case(case.id)
    g = CaseGroup.objects.get(name=groupname)
    g_id = g.id
    run_group_case(g_id)


def run_group_case(ids):
    '''
    运行组用例
    :param ids:
    :param name:
    :return:
    '''

    if ids:
        from .models import GroupResult
        obj, created = GroupResult.objects.get_or_create(group_id=ids)
        g = CaseGroup.objects.get(id=ids)
        cases = Case.objects.filter(case_group_id=ids)
        cases_ids = cases.values_list('id')
        case_id_all = [x[0] for x in cases_ids]
        t1 = datetime.datetime.now()
        num_run = 0
        rstatus = 1  # 未执行
        num_success = 0
        num_fail = 0
        num_error = 0
        num_all = 0
        for i in range(int(g.rerun) + 1):
            case_status_all = []
            run_all_case(case_id_all)

            for c in cases:
                if c.is_active == 2:
                    continue
                case_status_all.append(c.status)

            num_run = i
            num_success = case_status_all.count(2)
            num_fail = case_status_all.count(3)
            num_error = case_status_all.count(4)
            num_all = len(case_status_all)

            if 3 in case_status_all or 4 in case_status_all:
                rstatus = 3  # 失败
            else:
                rstatus = 2  # 成功
            if rstatus == 2:
                break

        # 总耗时

        obj.res_duration = getSecond(str(datetime.datetime.now() - t1))
        obj.res_rerun = num_run
        obj.res_success = num_success
        obj.res_fail = num_fail
        obj.res_error = num_error
        obj.res_status = rstatus
        obj.res_count = num_all
        obj.save()

        res_dict = {'code': 0, 'message': 'success', 'groupid': ids}
        return res_dict

@login_required()
def getGroupCase(request):
    '''获取某一个测试集合中的所有接口'''
    if request.method == 'GET':
        group_id = request.GET['group_id']
        if not group_id:
            msg = {'status': -2, 'error': 'group_id is null '}
            msg_json = json.dumps(msg, cls=DjangoJSONEncoder)
            return HttpResponse(msg_json)
        cases = Case.objects.get(case_group_id=group_id)
        cases_dict = {'status': 0, 'group_id': group_id, 'members': []}
        for case in cases:
            data = {
                    'request_method': case.request_method,
                    'params': case.params,
                    'headers': case.headers,
                    'is_active': case.is_active,
                    'update_time': case.update_time,
                    'expect_res': case.expect_res,
                    'fact_res': case.fact_res,
                    'duration': case.duration,
                    'status': case.status,

                    }
            case_dict = {
                'case_name': case.case_name,
                'case_id': case.id,
                'case_info': data
            }
            cases_dict['members'].append(case_dict)
        json_ss = json.dumps(cases_dict, cls=DjangoJSONEncoder)
        return HttpResponse(json_ss)

    else:
        msg = {'status': -1, 'error': 'request method is wrong, please use GET '}
        msg_json = json.dumps(msg, cls=DjangoJSONEncoder)
        return HttpResponse(msg_json)


@login_required()
def get_case_info(request):
    '''获取某一个接口的基本信息'''
    try:
        case_name = request.GET['case_name']
    except:
        return HttpResponse('You have no data !')

    try:
        case = Case.objects.get(case_name=case_name)
    except:
        return HttpResponse('no data, please check your case')

    data = {'case_name': case.case_name,
            'request_method': case.request_method,
            'params': case.params,
            'headers': case.headers,
            'is_active': case.is_active,
            'update_time': case.update_time,
            'expect_res': case.expect_res,
            'fact_res': case.fact_res,
            'duration': case.duration,
            'status': case.status,
            'case_group_id': case.case_group_id,
            }
    res_dict = {'status': 0, 'message': 'OK', 'data': data}
    json_ss = json.dumps(res_dict, cls=DjangoJSONEncoder)
    return HttpResponse(json_ss)





