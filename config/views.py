# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, HttpResponse, redirect
try :
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
import os
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from django.contrib.auth import get_user_model
from lib.log import log_level_dic
from .models import EmailConfig
from .forms import EmailConfigForm
from django.shortcuts import render, HttpResponseRedirect
try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse
from django.template.context import RequestContext

# Create your views here.

def get_token(request):
    if request.method == 'POST':
        new_token = get_user_model().objects.\
            make_random_password(length=12,
                allowed_chars='abcdefghjklmnpqrstuvwxyABCDEFGHJKLMNPQRSTUVWXY3456789')
        return HttpResponse(new_token)
    else:
        return True


@login_required()
@permission_verify()
def index(request):
    temp_name = 'config/config-header.html'
    display_control = 'none'
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    config = ConfigParser.ConfigParser()
    all_level = log_level_dic
    with open(dirs+'/AutoPlatMS.conf', 'r') as cfgfile:
        config.readfp(cfgfile)
        engine = config.get('db', 'engine')
        host = config.get('db', 'host')
        port = config.get('db', 'port')
        user = config.get('db', 'user')
        password = config.get('db', 'password')
        database = config.get('db', 'database')
        token = config.get('token', 'token')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')

    return render(request, 'config/index.html', locals())


@login_required()
@permission_verify()
def config_save(request):
    temp_name = 'config/config-header.html'
    if request.method == 'POST':
        engine = request.POST.get('engine')
        host = request.POST.get('host')
        port = request.POST.get('port')
        user = request.POST.get('user')
        password = request.POST.get('password')
        database = request.POST.get('database')
        token = request.POST.get('token')
        log_path = request.POST.get('log_path')
        log_level = request.POST.get('log_level')

        config = ConfigParser.RawConfigParser()
        dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        config.add_section('db')
        config.set('db', 'engine', engine)
        config.set('db', 'host', host)
        config.set('db', 'port', port)
        config.set('db', 'user', user)
        config.set('db', 'password', password)
        config.set('db', 'database', database)
        config.add_section('token')
        config.set('token', 'token', token)
        config.add_section('log')
        config.set('log', 'log_path', log_path)
        config.set('log', 'log_level', log_level)
        tips = u'保存成功！'
        display_control = ''
        conf_path = dirs + '/AutoPlatMS.conf'
        with open(conf_path, 'wb') as cfgfile:
            config.write(cfgfile)
        with open(conf_path, 'r') as cfgfile:
            config.readfp(cfgfile)
            engine = config.get('db', 'engine')
            host = config.get('db', 'host')
            port = config.get('db', 'port')
            user = config.get('db', 'user')
            password = config.get('db', 'password')
            database = config.get('db', 'database')
            token = config.get('token', 'token')
            log_path = config.get('log', 'log_path')
    else:
        display_control = 'none'
    return render(request, 'config/index.html', locals())

def get_dir(args):
    config = ConfigParser.RawConfigParser()
    dirs = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    conf_path = dirs + '/AutoPlatMS.conf'
    with open(conf_path, 'r') as cfgfile:
        config.readfp(cfgfile)
        token = config.get('token', 'token')
        log_path = config.get('log', 'log_path')
        log_level = config.get('log', 'log_level')

    # 根据传入参数返回变量以获取配置，返回变量名与参数名相同
    if args:
        return vars()[args]
    else:
        return HttpResponse(status=403)


@login_required
@permission_verify()
def email_list(request):
    temp_name = 'config/config-header.html'
    email_obj = EmailConfig.objects.all()
    return render(request, 'config/email_list.html', locals())


@login_required
@permission_verify()
def email_add(request):
    temp_name = 'config/config-header.html'
    if request.method == 'POST':
        e_form = EmailConfigForm(request.POST)
        if e_form.is_valid():
            e_form.save()
            tips = u"添加成功！"
            display_control = ""
            # return redirect("/config/email/list/")
            # return render(request, "config/email_add.html", locals())
        else:
            tips = u"增加失败！"
            display_control = ""
            return render(request, "config/email_add.html", locals())
    else:
        display_control = "none"
        e_form = EmailConfigForm()
    return render(request, "config/email_add.html", locals())


@login_required
@permission_verify()
def email_edit(request, ids):
    temp_name = 'config/config-header.html'
    edit_status = 0
    # if 判断有过滤对象则进行编辑修改，无对象则新建
    e_obj = EmailConfig.objects.filter(id=ids)
    if len(e_obj) == 1:
        e_obj = e_obj[0]
    else:
        e_obj = None

    if request.method.lower() == 'post':
        form = EmailConfigForm(request.POST, instance=e_obj)
        if form.is_valid():
            form.save()
            edit_status = 1
            tips = u'更新成功！'
            display_control = ''
        else:
            edit_status = 2
            tips = u'更新失败！'
            display_control = ''

    else:
        form = EmailConfigForm(instance=e_obj)
        display_control = "none"

    return render(request, 'config/email_edit.html', locals())



@login_required
@permission_verify()
def email_del(request, ids):
    '''
    :param request:
    :return:
    '''
    if ids:
        EmailConfig.objects.filter(id=ids).delete()
    return HttpResponseRedirect(reverse('email_list'), RequestContext(request))




















