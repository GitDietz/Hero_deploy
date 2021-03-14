import logging
import random
from django.db import connection

from coffee.models import Meetup, Member, MeetRecord

logger = logging.getLogger(__name__)

def make_permutations():
    """
    using only active members create the permutations of meetings
    """
    member_ids = list(Member.objects.active().order_by('id').values_list('id', flat=True))
    permutations = []
    while len(member_ids) > 1:
        for m in member_ids[1:]:
            permutations.append(str(member_ids[0]) + '|' + str(m))
        member_ids.pop(0)

    # now create this into the object Meetup
    for perm in permutations:
        Meetup.objects.create(combination=perm, active=True)

    new_objects = Meetup.objects.count()
    logger.info(f'Meetups created {new_objects}')
    return permutations


def record_meetup(in_lis_meeting_names):
    local_int_success = 1
    local_str_error = ''
    combined = ''
    try:
        for item in in_lis_meeting_names:
            combined += item + '\n'
        MeetRecord.objects.create(detail=combined)
        local_int_success = 0
    except Exception as e:
        local_str_error = f'{e}'
    finally:
        return local_int_success, local_str_error


def update_meetings(in_lis_mtg):
    """
    go update the meeting table with the meetings selected
    """
    logger.info("Start")
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
        logger.error(f'Error is {e}')
        local_str_error = f'{e}'
    finally:
        logger.info('END')
        return local_int_success, local_str_error, meetings_names


def get_db_value(in_sql_str, in_out_format_str):
    """
    Get a single value return from the DB, will fail if a set is returned
    :param in_sql_str: the raw query
    :param in_out_format_str: how the item should be returned
    :return:
    """
    logger.info('Start')
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
        logger.error(f'Issue found {e}')
        return None


def get_unique_pairs(in_lis_mtg, in_lis_members):
    """
    To find the first unique sets of meetings taking the items as they are in order
    Has application when there are a small number of options
    :param in_lis_mtg:
    :param in_lis_members:
    :return:
    """
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
    makes random selections from the available sets,
    checking that the members have not been set up for a meeting before
    in_lst_choices : pairs to pick from
    in_int_selections: number of combinations to add
    in_lst_already_chosen : combination pairs already selected
    """
    combinations = in_lst_already_chosen
    permutations = in_lst_choices
    individuals = get_individuals(in_lst_already_chosen)
    unique_pairs, all_individuals = get_unique_pairs(permutations, individuals)
    if len(unique_pairs) <= in_int_selections:
        logger.info('small set of pairs available')
        return 0, unique_pairs, all_individuals
    else:
        new_ppl = []
        while len(combinations) < in_int_selections:
            pick = random.choice(permutations)
            new_ppl = pick.split('|')
            if new_ppl[0] not in individuals and new_ppl[1] not in individuals:
                individuals.append(new_ppl[0])
                individuals.append(new_ppl[1])
                combinations.append(pick)
        return 0, combinations, individuals


def get_individuals(in_lst_combinations):
    logger.info('Start')
    individuals = []
    for pair in in_lst_combinations:
        members = pair.split('|')
        individuals.append(members[0])
        individuals.append(members[1])
    return individuals


def get_mtg_combinations(in_qs_mtg):
    logger.info('Start')
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
            meetings_now_reqd = meetings_required - meetings_set
            least_allocated = get_db_value('SELECT min(meetings) FROM coffee_meetup WHERE active = 1', 'int') + i
            qs_first_pool = Meetup.objects.done_times(least_allocated)
            local_int_success, local_list_pool_pairs, pool_mtg_keys = get_mtg_combinations(qs_first_pool)
            local_int_success, local_lis_mtgs, local_lis_individuals = get_random_pairs(local_list_pool_pairs,
                                                                                        meetings_now_reqd,
                                                                                        planned_mtgs)
            planned_mtgs.extend(local_lis_mtgs)
            meetings_found = len(planned_mtgs)
            meetings_set += meetings_found
            i += 1

        logger.info('meetings found {planned_mtgs}, all up {meetings_found}')
        local_int_success, local_str_error, local_lst_meetings = update_meetings(planned_mtgs)
        local_int_success, local_str_error = record_meetup(local_lst_meetings)
    except Exception as e:
        logger.error(f'Error in test : {e}')
    finally:
        # assuming we have enough meetings
        print('The following people are meeting:')
        for item in local_lst_meetings:
            print(f'{item}')
        return None

