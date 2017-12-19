# -*- coding:utf-8 -*-
from forms import CaseForm
from models import Case, CaseGroup, IS_ACTIVE, REQUEST_METHOD, REQUEST_TYPE, RESPONSE_STATUS, RESPONSE_TYPE, PROTOCOL
from django.shortcuts import render, HttpResponse, redirect
from django.db.models import Q
from api import get_object, get_case, api_request
from api import pages, str2gb
import csv, json , requests
import demjson
import datetime
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
import sys
reload(sys)
sys.setdefaultencoding('utf8')


@login_required()
@permission_verify()
def case(request):
    temp_name = "case/case-header.html"
    case_find = []
    case_info = Case.objects.all()
    group_info = CaseGroup.objects.all()
    request_types = REQUEST_TYPE
    request_methods = REQUEST_METHOD
    is_active_s = IS_ACTIVE
    status_s = RESPONSE_STATUS
    status = request.GET.get('status', '') # 接口状态:未执行，成功，失败，错误
    # case_name = request.GET.get('case_name', '') # 接口名称
    group_name = request.GET.get('case_group', '') # 从属项目
    # request_type = request.GET.get('request_type', '') # 请求类型
    request_method = request.GET.get('request_method', '') # 请求方法
    # ip = request.GET.get('ip', '') # 请求域名
    # # headers = request.GET.get('headers', '') # 请求头
    # # params = request.GET.get('params', '') # 请求参数
    is_active = request.GET.get('is_active', '') # 接口是否禁用
    # # add_time = request.GET.get('add_time', '') # 添加时间
    # # update_time = request.GET.get('update_time', '') # 更新时间
    # expect_res = request.GET.get('expect_res', '') # 预期结果
    # fact_res = request.GET.get('fact_res', '') # 实际结果
    keyword = request.GET.get('keyword', '') # 搜索关键词
    group_id = request.GET.get('group_id', '') # 组id
    export = request.GET.get('export', '') # 导出
    # # remark = request.GET.get('remark', '') # 备注
    # # duration = request.GET.get('duration', '') # 执行耗时
    # case_id = request.GET.get('case_id', '') # 用例ID
    # # proxies = request.GET.get('proxies', '')  # 代理
    case_id_all = request.GET.getlist('id', '')
    # update_index = request.GET.get('index', '')
    # 接口列表过滤规则
    if group_id:
        group = get_object(CaseGroup, id=group_id)
        if group:
            case_find = Case.objects.filter(group=group)
    else:
        case_find = Case.objects.all()

    if group_name:
        case_find = case_find.filter(case_group__name__contains=group_name)
    if is_active:
        case_find = case_find.filter(is_active__exact=is_active)
    if request_method:
        case_find = case_find.filter(request_method__exact=request_method)
    if status:
        case_find = case_find.filter(status__exact=status)
    # if expect_res:
    #     case_find = case_find.filter(expect_res__contains=expect_res)
    # if fact_res:
    #     case_find = case_find.filter(fact_res__contains=fact_res)
    # if remark:
    #     case_find = case_find.filter(remark__contains=remark)
    # Q() ---- 对对象的复杂查询 | 相当于 or
    if keyword:
        case_find = case_find.filter(
            Q(case_name__contains=keyword) |
            Q(ip__contains=keyword) |
            Q(case_group__name__contains=keyword) |
            Q(expect_res__contains=keyword) |
            Q(fact_res__contains=keyword) |
            Q(remark__contains=keyword) |
            Q(duration__contains=keyword)
        )
    if export:
        response = create_case_excel(export, case_id_all)
        return response



    # 所有对象， 分页器， 本页对象， 所有页码， 本页页码，是否显示第一页，是否显示最后一页
    all_obj, p, cases, page_range, current_page, show_first, show_end = pages(case_find, request)
    return render(request, 'case/index.html', locals())


def create_case_excel(export, case_id_all):
    # 导出选中
    if export == "true":
        if case_id_all:
            case_find = []
            for case_id in case_id_all:
                case_item = get_object(Case, id=case_id)
                if case_item:
                    case_find.append(case_item)
            response = HttpResponse(content_type='text/csv')

            now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
            file_name = 'atms_case_' + now + '.csv'
            response['Content-Disposition'] = "attachment; filename=" + file_name
            writer = csv.writer(response)
            writer.writerow([

                              str2gb(u'接口名称'), str2gb(u'用例组别'),
                              str2gb(u'协议'), str2gb(u'域名'),
                              str2gb(u'端口'), str2gb(u'路径'),
                              str2gb(u'请求方法'),
                              str2gb(u'请求头'), str2gb(u'请求参数'),
                              str2gb(u'是否禁用'), str2gb(u'更新时间'),
                              str2gb(u'预期结果'), str2gb(u'实际结果'),
                              str2gb(u'执行耗时'), str2gb(u'用例状态'),
                              str2gb(u'备注信息'), str2gb(u'代理地址'),
                              ])
            for c in case_find:
                if c.request_method:
                    c_req = int(c.request_method)
                    c_method = REQUEST_METHOD[c_req - 1][1]
                else:
                    c_method = ''
                if c.is_active:
                    c_at = int(c.is_active)
                    c_active = IS_ACTIVE[c_at - 1][1]
                else:
                    c_active = ''

                if c.status:
                    c_sta = int(c.status)
                    c_status = RESPONSE_STATUS[c_sta - 1][1]
                else:
                    c_status = ''

                group_obj = CaseGroup.objects.get(name=c.case_group)
                c_path = c.path
                c_protocol = PROTOCOL[int(c.protocol)][1] or PROTOCOL[int(group_obj.protocol)][1]
                print c_protocol
                c_ip = c.ip or group_obj.ip
                c_port = c.port or group_obj.port
                c_proxies = c.proxies or group_obj.proxies

                writer.writerow([
                                  str2gb(c.case_name), str2gb(c.case_group),
                                  str2gb(c_protocol), str2gb(c_ip),
                                  str2gb(c_port), str2gb(c_path),
                                  str2gb(c_method),
                                  str2gb(c.headers), str2gb(c.params),
                                  str2gb(c_active), str2gb(c.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                                  str2gb(c.expect_res), str2gb(c.fact_res),
                                  str2gb(c.duration), str2gb(c_status),
                                  str2gb(c.remark), str2gb(c_proxies),
                                  ])
            return response

    # 导出全部
    if export == 'all':
        case_all = Case.objects.all()
        response = HttpResponse(content_type='text/csv')

        now = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M')
        file_name = 'atms_case_' + now + '.csv'
        response['Content-Disposition'] = "attachment; filename=" + file_name
        writer = csv.writer(response)
        writer.writerow([
            str2gb(u'接口名称'), str2gb(u'用例组别'),
            str2gb(u'协议'), str2gb(u'域名'),
            str2gb(u'端口'), str2gb(u'路径'),
            str2gb(u'请求方法'),
            str2gb(u'请求头'), str2gb(u'请求参数'),
            str2gb(u'是否禁用'), str2gb(u'更新时间'),
            str2gb(u'预期结果'), str2gb(u'实际结果'),
            str2gb(u'执行耗时'), str2gb(u'用例状态'),
            str2gb(u'备注信息'), str2gb(u'代理地址'),
                         ])
        for c in case_all:
            if c.request_method:
                c_req = int(c.request_method)
                c_method = REQUEST_METHOD[c_req - 1][1]
            else:
                c_method = ''
            if c.is_active:
                c_at = int(c.is_active)
                c_active = IS_ACTIVE[c_at - 1][1]
            else:
                c_active = ''

            if c.status:
                c_sta = int(c.status)
                c_status = RESPONSE_STATUS[c_sta - 1][1]
            else:
                c_status = ''

            group_obj = CaseGroup.objects.get(name=c.case_group)
            c_path = c.path
            c_protocol = PROTOCOL[int(c.protocol)][1] or PROTOCOL[int(group_obj.protocol)][1]
            print c_protocol
            c_ip = c.ip or group_obj.ip
            c_port = c.port or group_obj.port
            c_proxies = c.proxies or group_obj.proxies

            writer.writerow([
                str2gb(c.case_name), str2gb(c.case_group),
                str2gb(c_protocol), str2gb(c_ip),
                str2gb(c_port), str2gb(c_path),
                str2gb(c_method),
                str2gb(c.headers), str2gb(c.params),
                str2gb(c_active), str2gb(c.update_time.strftime('%Y-%m-%d %H:%M:%S')),
                str2gb(c.expect_res), str2gb(c.fact_res),
                str2gb(c.duration), str2gb(c_status),
                str2gb(c.remark), str2gb(c_proxies),
                             ])
        return response


@login_required()
@permission_verify()
def case_add(request):
    temp_name = 'case/case-header.html'
    if request.method == 'POST':
        c_form = CaseForm(request.POST)
        # c_form.is_valid() 用户输入是否合法
        if c_form.is_valid():
            c_form.save()
            tips = u'增加成功！'
            display_control = ''
        else:
            tips = u'增加失败！'
            display_control = ''
        return render(request, 'case/case_add.html', locals())
    else:
        display_control = 'none'
        c_form = CaseForm()
        return render(request, 'case/case_add.html', locals())


@login_required()
@permission_verify()
def case_del(request):
    case_id = request.GET.get('id', '')
    # 直接删除
    if case_id:
        Case.objects.get(id=case_id).delete()

    # 删除勾选用例
    if request.method.lower() == 'post':
        case_batch = request.GET.get('arg', '')
        case_id_all = str(request.POST.get('case_id_all', ''))
        if case_batch:
            for case_id in case_id_all.split(','):
                case_item = get_object(Case, id=case_id)
                case_item.delete()

    return redirect("/casemanage/case/")


@login_required()
@permission_verify()
def case_run(request):
    case_id = request.GET.get('id', '')
    res = ()
    headers = {}
    proxies = {"http": None, "https": None}
    REQUEST_TYPE_DICT = dict(REQUEST_TYPE)
    if case_id:
        case_model = Case.objects.get(id=case_id)
        group_name = case_model.case_group
        case_is_active = case_model.is_active
        case_group = CaseGroup.objects.get(name=group_name)
        path = case_model.path

        protocol = case_model.protocol or case_group.protocol
        print 'protocol: ', protocol
        ip = case_model.ip or case_group.ip
        port = case_model.port or case_group.port

        if protocol == PROTOCOL[2][0]:  # PROTOCOL[2][0] == 2
            url = str(PROTOCOL[2][1]) + '://' + str(ip) + ':' + str(port) + str(path)

        else:
            url = str(PROTOCOL[1][1]) + '://' + str(ip) + ':' + str(port) + str(path)


        # content_type = case_model.content_type
        # case_is_active == 1 启用 ，2 禁用
        if case_is_active == 1:
            request_method_int = case_model.request_method
            if request_method_int == 1:
                request_method = 'GET'

            elif request_method_int == 2:
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
            # case_model.save()
            try:
                t1 = datetime.datetime.now()
                s = requests.session()
                res = api_request(session=s, method=request_method, url=url, params=params, headers=headers, proxies=proxies)
                res_status, res_response_message, res_rheaders, res_relapsed = res
                # 更新数据库中的字段，case_model.fact_res = res_response_message 所有字段都会被更新一次
                # Publisher.objects.filter(id=52).update(res_response_message='Apress Publishing') 只更新res_response_message其他不会被更新
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
            return HttpResponse(u'请先启用此用例')

    if request.method.lower() == 'post':
        case_batch = request.GET.get('arg', '')
        case_id_all = str(request.POST.get('case_id_all', ''))
        if case_batch:
            for case_id in case_id_all.split(','):
                case_model = get_object(Case, id=case_id)
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
    # 路由跳转用例列表界面
    return redirect("/casemanage/case/")


@login_required()
@permission_verify()
def case_edit(request, ids):
    case_methods = REQUEST_METHOD
    obj = get_object(Case, id=ids)
    mod_status = 0
    if request.method.lower() == 'post':
        cf = CaseForm(request.POST, instance=obj)

        if cf.is_valid():
            cf.save()
            mod_status = 1
        else:
            mod_status = 2

    else:
        cf = CaseForm(instance=obj)
    return render(request, 'case/case_edit.html', locals())


@login_required()
@permission_verify()
def case_info(request, ids):
    temp_name = 'case/case-header.html'
    obj = get_object(Case, id=ids)
    return render(request, 'case/case_info.html', locals())