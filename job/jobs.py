# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
# from django_celery_beat.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from djcelery.models import PeriodicTask, IntervalSchedule, CrontabSchedule
from django_celery_results.models import TaskResult
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from case.api import get_object
from forms import PeriodicTaskForm, IntervalForm, CrontabForm, TaskResultForm
from subprocess import Popen, PIPE
import os, time


@login_required
@permission_verify()
def index(request):
    temp_name = 'jobs/job_header.html'
    # 所有temp_name 会在base.html中被调用{% include temp_name %}
    jobs_info = PeriodicTask.objects.all()
    return render(request, 'jobs/job_list.html', locals())


@login_required
@permission_verify()
def job_edit(request, ids):
    status = 0
    obj = get_object(PeriodicTask, id=ids)
    if request.method == 'POST':
        form = PeriodicTaskForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            status = 1
        else:
            status = 2
    else:
        form = PeriodicTaskForm(instance=obj)

    return render(request, 'jobs/job_edit.html', locals())


@login_required
@permission_verify()
def job_add(request):
    temp_name = 'jobs/job_header.html'
    if request.method == 'POST':
        j_form = PeriodicTaskForm(request.POST)
        if j_form.is_valid():
            j_form.save()
            tips = u"添加成功！"
            display_control = ""
            return redirect("/jobs/job/list/")
        else:
            tips = u"增加失败！"
            display_control = ""
            return render(request, "jobs/job_add.html", locals())
    else:
        display_control = "none"
        j_form = PeriodicTaskForm()
        return render(request, "jobs/job_add.html", locals())


@login_required
@permission_verify()
def job_del(request):
    temp_name = "jobs/job_header.html"
    if request.method == 'POST':
        jobs = request.POST.getlist('jid_check',[])
        if jobs:
            for jid in jobs:
                PeriodicTask.objects.filter(id=jid).delete()
    jobs_info = PeriodicTask.objects.all()
    return render(request, "jobs/job_list.html", locals())


@login_required
@permission_verify()
def job_interval_list(request):
    temp_name = 'jobs/job_header.html'
    # 所有temp_name 会在base.html中被调用{% include temp_name %}
    interval_info = IntervalSchedule.objects.all()

    return render(request, 'jobs/job_interval_list.html', locals())


@login_required
@permission_verify()
def job_interval_add(request):
    temp_name = 'jobs/job_header.html'
    if request.method == 'POST':
        i_form = IntervalForm(request.POST)
        if i_form.is_valid():
            i_form.save()
            tips = u"添加成功！"
            display_control = ""
            # return redirect("/jobs/interval/add/")
        else:
            tips = u"添加失败！"
            display_control = ""
        # return render(request, "jobs/job_interval_add.html", locals())
    else:
        display_control = "none"
        i_form = IntervalForm()
    return render(request, "jobs/job_interval_add.html", locals())


@login_required
@permission_verify()
def job_interval_del(request):
    temp_name = "jobs/job_header.html"
    if request.method == 'POST':
        interval = request.POST.getlist('iid_check',[])
        if interval:
            for iid in interval:
                IntervalSchedule.objects.filter(id=iid).delete()
    interval_info = IntervalSchedule.objects.all()
    return render(request, "jobs/job_interval_list.html", locals())


@login_required
@permission_verify()
def job_interval_edit(request, ids):
    edit_status = 0
    obj = get_object(IntervalSchedule, id=ids)

    if request.method.lower() == 'post':
        form = IntervalForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            edit_status = 1
        else:
            edit_status = 2
    else:
        form = IntervalForm(instance=obj)

    return render(request, 'jobs/job_interval_edit.html', locals())


@login_required
@permission_verify()
def job_crontab_list(request):
    temp_name = 'jobs/job_header.html'
    # 所有temp_name 会在base.html中被调用{% include temp_name %}
    crontab_info = CrontabSchedule.objects.all()

    return render(request, 'jobs/job_crontab_list.html', locals())


@login_required
@permission_verify()
def job_crontab_add(request):
    temp_name = 'jobs/job_header.html'
    if request.method == 'POST':
        c_form = CrontabForm(request.POST)
        if c_form.is_valid():
            c_form.save()
            tips = u"添加成功！"
            display_control = ""
            # return redirect("/jobs/interval/add/")
        else:
            tips = u"添加失败！"
            display_control = ""
        # return render(request, "jobs/job_interval_add.html", locals())
    else:
        display_control = "none"
        c_form = CrontabForm()
    return render(request, "jobs/job_crontab_add.html", locals())


@login_required
@permission_verify()
def job_crontab_edit(request, ids):
    edit_status = 0
    obj = get_object(CrontabSchedule, id=ids)

    if request.method.lower() == 'post':
        form = CrontabForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            edit_status = 1
        else:
            edit_status = 2

    else:
        form = CrontabForm(instance=obj)

    return render(request, 'jobs/job_crontab_edit.html', locals())


@login_required
@permission_verify()
def job_crontab_del(request):
    temp_name = "jobs/job_header.html"
    if request.method == 'POST':
        crontab = request.POST.getlist('cid_check',[])
        if crontab:
            for cid in crontab:
                CrontabSchedule.objects.filter(id=cid).delete()
    crontab_info = CrontabSchedule.objects.all()
    return render(request, "jobs/job_crontab_list.html", locals())


@login_required
@permission_verify()
def job_result_list(request):
    temp_name = 'jobs/job_header.html'
    # 所有temp_name 会在base.html中被调用{% include temp_name %}
    # result_info = TaskResult.objects.all()
    # order_by 加 - 倒序排列
    result_info = TaskResult.objects.all().order_by('-date_done')

    return render(request, 'jobs/job_result_list.html', locals())


@login_required
@permission_verify()
def job_result_edit(request, ids):
    edit_status = 0
    obj = get_object(TaskResult, id=ids)

    if request.method.lower() == 'post':
        # form = TaskResultForm(request.POST, instance=obj)
        form = TaskResultForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            edit_status = 1
        else:
            edit_status = 2

    else:
        form = TaskResultForm(instance=obj)

    return render(request, 'jobs/job_result_edit.html', locals())


@login_required
@permission_verify()
def job_result_del(request):
    temp_name = "jobs/job_header.html"
    if request.method == 'POST':
        results = request.POST.getlist('tid_check', [])
        if results:
            for res in results:
                TaskResult.objects.filter(id=res).delete()
    result_info = TaskResult.objects.all()
    return render(request, "jobs/job_result_list.html", locals())


@login_required
@permission_verify()
def job_backend(request):
    temp_name = "jobs/job_header.html"
    celery_file = os.path.exists('/var/run/celery/w1.pid')
    beat_file = os.path.exists('/var/run/celery/beat.pid')
    if celery_file:
        celery_disable = "disabled"
        celery_stop_disable = ""
    else:
        celery_disable = ""
        celery_stop_disable = "disabled"
    if beat_file:
        beat_disable = "disabled"
        beat_stop_disable = ""
    else:
        beat_disable = ""
        beat_stop_disable = "disabled"
    return render(request, "jobs/job_backend.html", locals())


@login_required
@permission_verify()
def job_backend_task(request, name, action):
    """
       cmd1 = celery beat   -A AutoPlatMS -l info
       cmd2 = celery worker -A AutoPlatMS --loglevel=info
    """
    # cmd = name+" "+action+" -l info -b redis://localhost:6370"
    celery = 'celery'
    worker_dict = {
        'start': celery +' multi start w1 -E --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log',
        'stop': celery +" multi stop w1 -E --pidfile=/var/run/celery/%n.pid",
        'restart': celery +" multi restart w1 -E --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log",
        # 'stopwait': celery +" multi stopwait w1 -E -A AutoPlatMS --pidfile=/var/run/celery/%n.pid",
    }

    if name.lower() == 'worker':
        cmd = worker_dict[action]
    elif name.lower() == 'beat':
        if action.lower() == 'start':
            cmd = celery +' beat -A AutoPlatMS --pidfile=/var/run/celery/beat.pid --detach '
        elif action.lower() == 'stop':
            cmd = "pkill -9 -f 'celery beat' && rm -rf /var/run/celery/beat.pid"

        elif action.lower() == 'restart':
            cmd = "pkill -9 -f 'celery beat' && rm -rf /var/run/celery/beat.pid && " + celery \
                  +" beat -A AutoPlatMS --pidfile=/var/run/celery/beat.pid --detach"
    print cmd
    r = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
    rc = r.communicate()
    print rc[0]
    time.sleep(3)
    cmd2 = 'whoami'
    r1 = Popen(cmd2, stdout=PIPE, stderr=PIPE, shell=True)
    rc1 = r1.communicate()
    print rc1[0]
    return redirect("/jobs/job/backend/")