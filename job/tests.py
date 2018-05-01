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
import logging
logger = logging.getLogger(__name__)

