from django.shortcuts import render, HttpResponse

# Create your views here.

from job import tasks


def task_test(request):
    res = tasks.add.delay(228, 24)
    print("start running task")
    print("async task res", res.get())

    return HttpResponse('res %s' % res.get())