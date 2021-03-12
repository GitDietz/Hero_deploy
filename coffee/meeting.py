import random
from django.db import connection

from coffee.models import Meetup, Member

def make_permutations():
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


def update_meetings(in_lis_mtg):
    """
    go update the meeting tbale with the meetings selected
    """
    local_int_success = 1
    local_str_error = ''
    meetings_names = []
    try:
        for item in in_lis_mtg:
            ppl = item.split('|')
            person_1 = Member.objects.get(pk=int(ppl[0])).full_name
            person_2 = Member.objects.get(pk=int(ppl[1])).full_name
            meetings_names.append(person_1 + ' meeting ' + person_2)
            item_model = Meetup.objects.get(combination=item)
            item_model.increment()

        local_int_success = 0
    except Exception as e:
        local_str_error = f'{e}'
    finally:
        pass
        return local_int_success, local_str_error, meetings_names



def get_db_value(in_sql_str, in_out_format_str):
    try:
        with connection.cursor() as cursor:
            cursor.execute(in_sql_str)
            result = cursor.fetchone()[0]
        if in_out_format_str == 'str':
            return str(result)
        elif in_out_format_str == 'int':
            return int(result)
        else:
            return result
    except Exception as e:
        print(f'Issue found {e}')
        return None


def get_unique_pairs(in_lis_mtg, in_lis_members):
    unique = []
    members = in_lis_members
    for mtg in in_lis_mtg:
        mtg_member = mtg.split('|')
        if mtg_member[0] not in members and mtg_member[1] not in members:
            members.append(mtg_member[0])
            members.append(mtg_member[1])
            unique.append(mtg)
    return unique, members


def get_random_pairs(in_lst_choices, in_int_selections, in_lst_already_chosen):
    """
    in_lst_choices : pairs to pick from
    in_int_selections: number of combinations to add
    in_lst_already_chosen : combination pairs already selected
    """
    combinations = in_lst_already_chosen
    permutations = in_lst_choices
    individuals = get_individuals(in_lst_already_chosen)
    unique_pairs, all_individuals = get_unique_pairs(permutations, individuals)
    if len(unique_pairs) <= in_int_selections:
        return 0, unique_pairs, all_individuals
    else:
        new_ppl = []
        while len(combinations) < in_int_selections:
            # this forms an infinte loop on low selection options
            # nee a method to find unique members available
            pick = random.choice(permutations)
            new_ppl = pick.split('|')
            # print(f'the new selection {new_ppl}')
            if new_ppl[0] not in individuals and new_ppl[1] not in individuals:
                individuals.append(new_ppl[0])
                individuals.append(new_ppl[1])
                combinations.append(pick)
                # print(f'individuals are now {individuals}')
        # print(f' final combination is = {combinations}')
        return 0, combinations, individuals


def get_individuals(in_lst_combinations):
    individuals = []
    for pair in in_lst_combinations:
        members = pair.split('|')
        individuals.append(members[0])
        individuals.append(members[1])
    return individuals


def get_mtg_combinations(in_qs_mtg):
    local_int_success = 1
    meeting_combinations = []
    meeting_pks = []
    try:
        for item in in_qs_mtg:
            meeting_combinations.append(item.combination)
            meeting_pks.append(item.pk)
        local_int_success = 0
    except Exception as e:
        print(f'Error: {e}')
    finally:
        return local_int_success, meeting_combinations, meeting_pks


def test_old():
    """
    work out the logic for the meeting schedule
    get those combinations that are 2nd highest allocation, from them create
    meetings to satisfy the number to set.
    if the 2nd highest list < required just allocate them and then create the additional
    :param request:
    :return:
    """
    planned_mtgs = [] # to be a list of strings that represent pks for the members
    selected_mtg_pks = []
    """
    replan this - cant take all the remaining unallocted mtgs because the individuals may create duplicates
    each cycle will have to start at the lowest allocated mtgs, try those, then step up t the next count level 
    and so on until the reuired mtgs are set
    """
    try:
        meetins_required = Member.meetings_to_set()
        max_mtg_now = get_db_value('SELECT max(meetings) FROM coffee_meetup WHERE active = 1', 'int')
        if max_mtg_now > 0:
            # look for under allocated meeting combinations
            next_max_mtg_now = get_db_value(f'SELECT max(meetings) FROM coffee_meetup WHERE active = 1 and meetings < {max_mtg_now}', 'int')
            qs_firstlot_mtgs = Meetup.objects.done_times(next_max_mtg_now)
        else:
            # messages.error(request, 'no meetings set so far')
            qs_firstlot_mtgs = Meetup.objects.done_times(max_mtg_now)

        if qs_firstlot_mtgs.count() < meetins_required:
            # add this to the list of meeting to arrange now
            local_int_success, new_mtgs, meeting_pks = get_mtg_combinations(qs_firstlot_mtgs)
            planned_mtgs.extend(new_mtgs)
            print(f'Planned mtgs {planned_mtgs}')
            selected_mtg_pks.extend(meeting_pks)
            # then run operation on full set again to get the additional
            qs_2ndlot_mtgs = Meetup.objects.done_times(next_max_mtg_now-1)
            # get random selection from this
            local_int_success, new_2ndlot_mtgs, meeting_2ndlot_pks = get_mtg_combinations(qs_2ndlot_mtgs)

            pass
        elif qs_firstlot_mtgs.count() == meetins_required:
            # this is all the meetings required, return it and stop
            planned_mtgs = qs_firstlot_mtgs.combination
            pass
        else:
            # make selection
            # local_int_success, new_combinations = get_pairs(qs_firstlot_mtgs, meetins_required, [])
            pass
        # now the email have to be sent and the meetups have to be updated
        # now have the potential list get meetings from it
    except Exception as e:
        print(f'Error : {e}')
    return None


def test():
    planned_mtgs = []  # to be a list of strings that represent pks for the members
    selected_mtg_keys = []
    selected_member_keys = []
    # local_lis_mtgs looks like this  ['12|15', '2|16', '11|14', '5|9', '7|13', '3|8', '4|6']
    try:
        meetings_required = Member.meetings_to_set()
        meetings_set = 0
        i = 0
        local_lis_individuals = []
        while meetings_required > meetings_set:
            meetings_now_reqd = meetings_required = meetings_set
            least_allocated = get_db_value('SELECT min(meetings) FROM coffee_meetup WHERE active = 1', 'int') + i
            qs_first_pool = Meetup.objects.done_times(least_allocated)
            local_int_success, local_list_pool_pairs, pool_mtg_keys = get_mtg_combinations(qs_first_pool)
            # insert meetings_now_reqd below
            local_int_success, local_lis_mtgs, local_lis_individuals = get_random_pairs(local_list_pool_pairs,
                                                                                        meetings_required,
                                                                                        local_lis_individuals)
            planned_mtgs.extend(local_lis_mtgs)
            meetings_found = len(planned_mtgs)
            meetings_set =+ meetings_found

        print(f'meetings found {planned_mtgs}, all up {meetings_found}')
        local_int_success, local_str_error, local_lst_meetings = update_meetings(planned_mtgs)

        # also get the pks for the combinations, then go and update them and send emails

    except Exception as e:
        print(f'Error in test : {e}')
    finally:
        # assuming we have enough meetings
        print('The following people are meeting:')
        for item in local_lst_meetings:
            print(f'{item}')
        return None

