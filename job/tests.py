# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TestCase

# Create your tests here.
from subprocess import *
import commands, os
# cmd = "celery multi start w1 -E --pidfile=/var/run/celery/%n.pid --logfile=/var/log/celery/%n%I.log"
# # cmd = 'ps -A |grep celery'
# # cmd = 'pkill -9 -f "celery worker"'
# print cmd
# # out = os.system(cmd)
# p = Popen(cmd, stdout=PIPE, stderr=PIPE, shell=True)
# out = p.communicate()
# print out[0]
# print ">>>>>>>>>>>>>>>>"


def gete(*args):
    if isinstance(args, tuple):
        print 'YES'
    print type(args)
    for i in args:
        print i
    # print args

a = [1,2,3]
b = 1
c =2
gete(b)