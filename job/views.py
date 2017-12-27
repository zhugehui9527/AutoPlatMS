from django.shortcuts import render, HttpResponse

# Create your views here.

from tasks import add


def task_test(request):
    res = add.delay(228, 24)
    print("start running task")
    print("async task res", res.get())

    return HttpResponse('res %s' % res.get())