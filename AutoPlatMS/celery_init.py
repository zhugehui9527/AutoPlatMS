# -*- coding:utf-8 -*-
from __future__ import absolute_import, unicode_literals
import os,django
from celery import Celery, platforms

from django.conf import settings


#获取当前文件夹名，即为该Django的项目名
project_name = os.path.split(os.path.abspath('.'))[-1]
project_settings = '%s.settings' % project_name

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)

# 解决django.core.exceptions.AppRegistryNotReady: Apps aren't loaded yet.
# django.setup()

app = Celery(project_name)

# app.conf.update(
#     task_serializer='json',
#     accept_content=['json'],  # Ignore other content
#     result_serializer='json',
#     timezone='Europe/Oslo',
#     enable_utc=True,
#     beat_scheduler='djcelery.schedulers.DatabaseScheduler',
#     broker_url='redis://localhost:6379/0',
#     result_backend='django-db',
#
# )


# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix. namespace='CELERY'

output = os.popen('celery --version').read()
if '4.' in output:
    app.config_from_object('django.conf:settings', namespace='CELERY')
    app.autodiscover_tasks()
else:
    app.config_from_object('django.conf:settings')
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


# to get root privilege
platforms.C_FORCE_ROOT = True


# 只有bind=True时， task对象会作为第一个参数自动传入。
@app.task(bind=False)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


