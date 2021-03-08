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


def meet_test(request):
    thing = Meetup.active_individuals()
    other = 8