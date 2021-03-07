from django.shortcuts import render

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


def member_list(request):
    members = Member.objects.all()
    template = ''
    pass


def member_new(request):
    pass


def member_edit(request):
    pass
