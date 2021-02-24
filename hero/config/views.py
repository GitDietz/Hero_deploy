from django.http import HttpResponse
from django.shortcuts import render
import datetime

# from .models import Task

def current_datetime(request):
    now = datetime.datetime.now()
    html = "<html><body>It is now %s.</body></html>" % now
    return HttpResponse(html)


# def task_list(request):
#     objects = Task.objects.all()
#     template = 'pages/list.html'
#     context = {
#         'objects': objects,
#     }
#     return render(request, template, context)

def time(request):
    template = 'pages/list.html'
    now = datetime.datetime.now()
    context = {
        'time': now,
    }
    return render(request, template, context)
