from django.db import connection
from django.shortcuts import render, redirect

from .models import Meetup, Member


def make_permutations(request):
    """
    using only active members
    :param request:
    :return:
    """
    member_ids = list(Member.objects.active().order_by('id').values_list('id', flat=True))
    original = member_ids
    permutations = []
    while len(member_ids) > 1:
        for m in member_ids[1:]:
            # print(m)
            permutations.append(str(member_ids[0]) + '|' + str(m))
        member_ids.pop(0)

    print(permutations)
    # now create this into the object Meetup
    for perm in permutations:
        Meetup.objects.create(combination=perm, active=True)

    new_objects = Meetup.objects.count()
    print(f'Meetups created {new_objects}')
    return permutations


def get_individuals():
    """
    Using the passed in list of combinations get the list of individual ids
    :return:
    """
    # while len(combinations) < divo[0]:
#     pick = random.choice(permutations)
#     its = pick.split('|')
#     print(f'the new selection {its}')
#     if its[0] not in individuals and its[1] not in individuals:
#         individuals.append(its[0])
#         individuals.append(its[1])
#         combinations.append(pick)

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


def get_db_value(in_sql_str):
    with connection.cursor() as cursor:
        cursor.execute(in_sql_str)
        result = cursor.fetchone()
    return result


def meet_test(request):
    """
    work out the logic for the meeting schedule
    get those combinations that are 2nd highest allocation, from them create
    meetings to satisfy the number to set.
    if the 2nd highest list < required just allocate them and then create the additional
    :param request:
    :return:
    """
    # thing = Meetup.active_individuals()
    meetins_required = Member.meetings_to_set()
    # with connection.cursor() as cursor:
    #     cursor.execute('SELECT max(meetings) FROM coffee_meetup WHERE active = 1')
    #     max_meet = cursor.fetchone()
    max_meet = get_db_value('SELECT max(meetings) FROM coffee_meetup WHERE active = 1')
    if max_meet > 0:
        next_max_mtg = get_db_value('SELECT max(meetings) FROM coffee_meetup WHERE active = 1 and meetings < 2')
    # max_meet = Meetup.highest_mtgs()
    next_max_mtg = Meetup.next_highest_mtgs()
    underallocated_mtgs = Meetup.objects.done_times(2)
    return redirect('home')