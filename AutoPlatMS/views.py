# -*- coding:utf-8 -*-
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.response import Response


def index(request):
    # render是渲染变量到模板中,而redirect是HTTP中的1个跳转的函数,一般会生成302状态码
    return redirect('/dash/dashboard/index/')


def empty_view(request):
    content = {'please move along': 'nothing to see here'}
    return Response(content, status=status.HTTP_404_NOT_FOUND)