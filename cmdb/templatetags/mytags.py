# -*- coding:utf-8 -*-
from django import template
register = template.Library()


@register.filter(name='int2str')
def int2str(value):
    '''
    int 转换为 str
    :param value:
    :return:
    '''
    return str(value)

@register.filter(name='res_splict')
def res_split(value):
    '''
    将结果格式化换行
    :param value:
    :return:
    '''
    res = []
    if isinstance(value, tuple):
        for v in value:
            if v is not None:
                data = v.replace('\n', '<br>')
                res.append(data)
        return res
    else:
        return value
