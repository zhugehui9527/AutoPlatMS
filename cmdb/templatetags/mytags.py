# -*- coding:utf-8 -*-
from django import template
register = template.Library()



@register.filter(name='bool2str')
def bool2str(isbool):
    '''
    bool 转换为 str
    :param value:
    :return:
    '''
    if isbool:
        return '是'
    else:
        return '否'


@register.filter(name='int2str')
def int2str(value):
    '''
    request method
    :param value:
    :return:
    '''
    if value == 1:
        return 'GET'
    elif value == 2:
        return 'POST'


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


@register.filter(name='filter_state')
def filter_state(result_info, taskname):
    '''
    过滤出task中某一个的state
    :param taskname:
    :param job:
    :return:
    '''
    for res in result_info:
        if res.task == taskname:
            return res.state
        else:
            return None



