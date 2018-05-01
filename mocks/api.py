# -*- coding: utf-8 -*-
from rest_framework import serializers, routers, viewsets
from mocks.models import MockGroup, Mock
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
import requests
try:
    import json
except ImportError as e:
    import simplejson as json

class MockGroupSerial(serializers.ModelSerializer):
    class Meta:
        model = MockGroup
        fields = '__all__'

class MockSerial(serializers.ModelSerializer):
    '''Mock 序列化'''
    # group = MockGroupSerial(many=True, read_only=True)
    # CharField(source='<本model中的外键>.<外键指向的model的相应属性>')
    # group = serializers.CharField(source='mockgroup.name')
    class Meta:
        model = Mock
        # __all__ 全部， 如果只想显示某些用 ('id', 'name')
        fields = '__all__'
        # depth = 1  # 遍历深度
        # read_only_fields = ()


def mock_one_run(request, ids):
    '''
    mock run
    :param request:
    :param ids:
    :return:
    '''
    m = Mock.objects.filter(id=ids)
    path = m.path
    param = m.params
    data_json = json.dumps(param, cls=DjangoJSONEncoder)
    host = request.get_host()
    url = 'http://' + host + '/mock/mock_api/' + path
    method = m.request_method
    headers = None
    if not m.headers:
        headers = m.headers

    if method == 1:
        res = requests.get(url=url, params=param, headers=headers)
        return res.content
    if method == 2:
        res = requests.post(url=url, data=data_json, headers=headers)
        return res.content


def get_group_memebers(request):
    if request.GET:
        d = []
        try:
            group_name = request.GET['name']
        except:
            return HttpResponse('your parameter is error')
        if group_name == 'all':
            case_groups = MockGroup.objects.all()
            for cg in case_groups:
                ret_cg = {'mock_group': cg.name, 'memebers':[]}
                memebers = Mock.objects.filter(group__name=cg.name)
                for c in memebers:
                    ret_c = {'mock_name': c.name, }
                    ret_cg['members'].append(ret_c)
                d.append(ret_cg)
            return HttpResponse(json.dumps(d))
        else:
            ret_cg = {'mock_group': group_name, 'memebers':[]}
            memebers = Mock.objects.filter(group__name=group_name)
            for c in memebers:
                ret_c = {'mock_name': c.name, }
                ret_cg['memebers'].append(ret_c)
            d.append(ret_cg)
            return HttpResponse(json.dumps(d))
    return HttpResponse(status=403)
