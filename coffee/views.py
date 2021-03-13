import logging

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.shortcuts import render, redirect

from .models import Meetup, Member
from .meeting import test

logger = logging.getLogger(__name__)

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
    template = 'member.html'
    try:
        member = Member.objects.get(pk=pk)
        context = {
            'title': 'Edit the member detail',
            'object': member,
        }
        return render(request, template, context)
    except ObjectDoesNotExist:
        redirect('member_list')


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

    """
    result = test()

    return redirect('home')