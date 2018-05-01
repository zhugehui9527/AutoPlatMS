# -*- coding: utf-8 -*-

from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import Case, CaseGroup, GroupResult
from .forms import GroupForm, CaseForm
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from .api import get_object, run_all_case
import datetime
from django.core.serializers.json import DjangoJSONEncoder
from django.http import Http404
try:
    import json
except ImportError as e:
    import simplejson as json

@login_required()
@permission_verify()
def group(request):
    '''获取所有案例集'''
    temp_name = "case/case-header.html"
    allgroup = CaseGroup.objects.all()
    return render(request, 'case/group.html', locals())


@login_required()
@permission_verify()
def group_add(request):
    '''添加案例集（组）'''
    temp_name = "case/case-header.html"
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
        return render(request, 'case/group_add.html', locals())
    else:
        display_control = "none"
        group_form = GroupForm()
        return render(request, 'case/group_add.html', locals())


@login_required()
@permission_verify()
def group_edit(request, ids):
    '''编辑案例集'''
    obj = get_object_or_404(CaseGroup, id=ids)
    allgroup = CaseGroup.objects.all()
    unselect = Case.objects.filter(case_group__name=None)
    members = Case.objects.filter(case_group__name=obj.name)
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
    return render(request, 'case/group_edit.html', locals())


@login_required()
@permission_verify()
def group_run(request):
    '''运行案例集'''
    if request.method == 'POST':
        ids = int(request.POST.get('ids', ''))
        if ids:
            from .api import run_group_case
            res = run_group_case(ids)
            msg_json = json.dumps(res, cls=DjangoJSONEncoder)
            return HttpResponse(msg_json)
        else:
            return HttpResponse('have no data')
    else:
        return HttpResponse('please use post to request')


@login_required()
def group_info(request, ids):
    '''案例集详情'''
    temp_name = 'case/case-header.html'
    obj = get_object(CaseGroup, id=ids)
    members = Case.objects.filter(case_group_id=ids)
    return render(request, 'case/group_info.html', locals())


@login_required()
@permission_verify()
def group_del(request):
    '''案例集删除'''
    temp_name = 'case/case-header.html'
    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        group_id = request.POST.get("id", "")
        if group_id:
            CaseGroup.objects.get(id=group_id).delete()
        if group_items:
            for n in group_items:
                CaseGroup.objects.get(id=n).delete()
    allgroup = CaseGroup.objects.all()
    return render(request, 'case/group.html', locals())


@login_required()
@permission_verify()
def group_save(request):
    '''案例集保存'''
    temp_name = 'case/case-header.html'
    mod_status = 0
    if request.method == 'POST':
        group_id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        proxies = request.POST.get('proxies')
        port = request.POST.get('port')
        ip = request.POST.get('ip')
        rerun = request.POST.get('rerun')
        protocol = request.POST.get('protocol')
        members = request.POST.getlist('members', [])
        unselect = request.POST.getlist('unselect', [])
        group_item = CaseGroup.objects.get(id=group_id)
        if unselect:
            for case in unselect:
                obj = Case.objects.get(case_name=case)
                obj.case_group_id = None
                obj.save()
        if members:
            for case in members:
                obj = Case.objects.get(case_name=case)
                obj.case_group_id = group_id
                obj.save()
        group_item.name = name
        group_item.desc = desc
        group_item.proxies = proxies
        group_item.ip = ip
        group_item.port = port
        group_item.protocol = protocol
        group_item.rerun = rerun
        group_item.save()
        obj = group_item
        mod_status = 1
    else:
        mod_status = 2

    return render(request, 'case/group_edit.html', locals())



@login_required()
@permission_verify()
def group_result(request):
    '''案例集保存'''
    temp_name = 'case/case-header.html'
    result = GroupResult.objects.all()
    return render(request, 'case/result.html', locals())


@login_required()
@permission_verify()
def result_del(request):
    '''案例集删除'''
    temp_name = 'case/case-header.html'
    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        group_id = int(request.POST.get("id", ""))
        if group_id:
            GroupResult.objects.get(id=group_id).delete()
        if group_items:
            for n in group_items:
                GroupResult.objects.get(id=int(n)).delete()

    return render(request, 'case/result.html', locals())