# -*- coding: utf-8 -*-

from django.shortcuts import render
from models import Case, CaseGroup
from forms import GroupForm, CaseForm
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from api import get_object


@login_required()
@permission_verify()
def group(request):
    temp_name = "case/case-header.html"
    allgroup = CaseGroup.objects.all()
    # context = {
    #     'temp_name': temp_name,
    #     'allgroup': allgroup,
    # }
    return render(request, 'case/group.html', locals())


@login_required()
@permission_verify()
def group_add(request):
    temp_name = "case/case-header.html"
    if request.method == 'POST':
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
    obj = get_object(CaseGroup, id=ids)
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
def group_del(request):
    temp_name = 'case/case-header.html'

    if request.method == 'POST':
        group_items = request.POST.getlist('g_check', [])
        group_id = request.POST.get("id", "")
        if group_id:
            CaseGroup.objects.get(id=group_id).delete()
        if group_items:
            for n in group_items:
                CaseGroup.objects.filter(id=n).delete()
    allgroup = CaseGroup.objects.all()
    return render(request, 'case/group.html', locals())

#
@permission_verify()
def group_save(request):
    temp_name = 'case/case-header.html'
    mod_status = 0
    if request.method == 'POST':
        group_id = request.POST.get('id')
        name = request.POST.get('name')
        desc = request.POST.get('desc')
        proxies = request.POST.get('proxies')
        port = request.POST.get('port')
        ip = request.POST.get('ip')
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
        print group_item.proxies
        group_item.ip = ip
        group_item.port = port
        group_item.protocol = protocol
        group_item.save()
        obj = group_item
        mod_status = 1
    else:
        mod_status = 2

    return render(request, 'case/group_edit.html', locals())





