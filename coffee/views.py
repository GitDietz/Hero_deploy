import logging

from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import connection
from django.shortcuts import render, redirect

from .forms import MeetingForm, MemberForm
from .models import Meetup, Member, MeetRecord
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
    template = 'member.html'
    form = MemberForm()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            redirect('member_list')
        else:
            logger.error(f'Form: {form.errors}')

    context = {
        'title': 'Edit the member detail',
        'form': form,
    }
    return render(request, template, context)


def member_edit(request, pk):
    template = 'member.html'

    try:
        member = Member.objects.get(pk=pk)
        form = MemberForm(instance=member)
        if request.method =='POST':
            if form.is_valid():
                form.save()
                redirect('member_list')
            else:
                logger.error(f'Form: {form.errors}')

        context = {
            'title': 'Edit the member detail',
            'object': member,
            'form': form,
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


def meetup_list(request):
    objects = Meetup.objects.all()[:3]
    template = 'member_list.html'
    context = {
        'title': 'Meetups list',
        'objects': objects,
    }
    return render(request, template, context)


def make_meetings(request):
    pass


def meet_test(request):
    """

    """
    result = test()

    return redirect('home')