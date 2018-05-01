# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase



# Create your tests here.


# import requests, requests_mock
# session = requests.session()
# adapter = requests_mock.Adapter()
# session.mount('mock', adapter)
# adapter.register_uri(method='GET', url='mock://127.0.0.1:3000/1/2/3', text='code:0')
# resp = session.get('mock://127.0.0.1:3000/1/2/3')
# print resp.status_code, resp.text

task_id = '6490751f-7548-4ac6-be61-cec599a50f5b'
import requests
state_ = requests.get('http://127.0.0.1:8000/jobs/job/getstate/{}/'.format(task_id))
state_json = state_.json()

name = state_json['name']
buildid = state_json['id']
state = state_json['state']
a = [False, True, True]
print(name)
print(all(x for x in a))