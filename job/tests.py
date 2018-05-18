# -*- coding: utf-8 -*-
from __future__ import unicode_literals

# from django.test import TestCase

# Create your tests here.
# from .views import DumpCam

# from celery import Celery


# def my_monitor(app):
#     state = app.events.State()
#
#     def announce_failed_tasks(event):
#         state.event(event)
#         # task name is sent only with -received event, and state
#         # will keep track of this for us.
#         task = state.tasks.get(event['uuid'])
#         print('TASK FAILED: %s[%s] %s' % (
#             task.name, task.uuid, task.info(),))
#
#     with app.connection() as connection:
#         recv = app.events.Receiver(connection, handlers={
#                 'task-succeeded': announce_failed_tasks,
#                 '*': state.event,
#         })
#         recv.capture(limit=None, timeout=None, wakeup=True)

# if __name__ == '__main__':
#     app = Celery(broker='redis://localhost:6379/0')
#     my_monitor(app)
tulp1 = {'test_2': '124', 'test_4': '185','test_1': '195', 'test_3': '26', 'test_5': '489'}
tulp2 = {'test_2': '124', 'test_4': '185','test_5': '489'}

a = sorted(tulp1.items(), key=lambda x:x[0], reverse=False)
a1 = dict(a)

b = sorted(tulp2.items(), key=lambda x:x[0], reverse=False)
b1 = dict(b)

def isIn(x,y):
    x = set(x)
    y = set(y)
    len_x = len(x)
    len_y = len(y)
    if len_x >= len_y:
        if x & y == y:
            return True
        else:
            return False
    else:
        if x & y == x:
            return True
        else:
            return False

def cmp_dict(dict1, dict2):
    x = set(dict1.items())
    y = set(dict2.items())
    x1 = set(dict1.keys())
    y1 = set(dict1.keys())
    len_x = len(x)
    len_y = len(y)
    if len_x >= len_y:
        if (x & y == y) and (x1 & y1 == y1):
            return True
        else:
            return False
    else:
        if (x & y == x) and (x1 & y1 == x1):
            return True
        else:
            return False


print(cmp_dict(a1, b1))

