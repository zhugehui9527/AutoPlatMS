# -*- coding:utf-8 -*-
from django.shortcuts import redirect


def index(request):
    # render是渲染变量到模板中,而redirect是HTTP中的1个跳转的函数,一般会生成302状态码
    return redirect('/navi/')
