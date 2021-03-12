import random

from django.contrib import messages
from django.db import connection
from django.shortcuts import render, redirect

from .models import Meetup, Member
from .meeting import test


def member_list(request):
    objects = Member.objects.all()
    template = 'member_list.html'
    context = {
        'title': 'Member list',
        'objects': objects,
    }
    return render(request, template, context)


def member_new(request):
    pass


def member_edit(request, pk):
    member = Member.objects.get(pk=pk)

    pass


def combination_list(request):
    objects = Meetup.objects.all()
    template = 'combination_list.html'
    context = {
        'title': 'Meetup list',
        'objects': objects,
    }
    return render(request, template, context)



def meet_test(request):
    """
    work out the logic for the meeting schedule
    get those combinations that are 2nd highest allocation, from them create
    meetings to satisfy the number to set.
    if the 2nd highest list < required just allocate them and then create the additional
    :param request:
    :return:
    """
    result = test()

    return redirect('home')