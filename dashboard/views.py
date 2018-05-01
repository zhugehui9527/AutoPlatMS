# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from accounts.permission import permission_verify
from case.models import CaseGroup, Case
from mocks.models import Mock, MockGroup

import sys, os
if sys.version_info <(3,0):
    reload(sys)
    sys.setdefaultencoding('utf8')

# Create your views here.


@login_required()
@permission_verify()
def show_index(request):
    temp_name = "dashboard/dash-header.html"
    case_group_all = CaseGroup.objects.all().count()
    case_api_all = Case.objects.all().count()
    mock_group_all = MockGroup.objects.all().count()
    mock_api_all = Mock.objects.all().count()
    return render(request, 'dashboard/index.html', locals())