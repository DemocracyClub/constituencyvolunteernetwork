try:
    import json
except ImportError:
    import simplejson as json
from itertools import chain

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from signup.models import CustomUser
from signup.util import render_with_context
from tasks.util import login_key
from models import YNMPAction
from signals import ynmp_action_done
from util import ynmp_login_url

def _build_board(count=None,
                 with_user_ob=False):
    users = CustomUser.objects.order_by('-points')\
            .exclude(points=0)
    if count:
        users = users[:count]
    leader_board = []
    position = 1
    for user in users:
        data = {'name': user.display_name,
                'points': user.points,
                'dc_user_id': user.id,
                'position': position}
        if with_user_ob:
            data['user'] = user
        leader_board.append(data)
        position += 1
    return leader_board
    
def _build_leader_board():
    return _build_board(count=5)

def _build_contextual_board(user):
    users = CustomUser.objects.order_by('-points')
    lower = users\
            .filter(points__lt=user.points)[:2]
    higher = users\
             .order_by('points')\
             .filter(points__gt=user.points)
    count_higher = higher.count()
    higher = higher[:2]
    lower.reverse()
    leader_board = []
    position = count_higher - 1
    for user in chain(higher, [user], lower):
        leader_board.append({'name': user.display_name,
                             'points': user.points,
                             'position': position,
                             'dc_user_id': user.id})
        position += 1
    return leader_board

def _build_json_response(user):
    response = {}
    response['dc_user_id'] = user.id
    response['total_points'] = user.points
    response['leader_board'] = _build_leader_board()
    response['contextual_board'] = _build_contextual_board(user)
    response['full_table_url'] = reverse('ynmp_table')

    return json.dumps(response)

def table(request):
    context = {}
    context['full_table'] = _build_board(with_user_ob=True)
    return render_with_context(request,
                               'table.html',
                               context)


def api(request):
    if 'dc_user_id' not in request.REQUEST or 'points_awarded' not in request.REQUEST:
        return HttpResponseBadRequest()

    dc_user_id = int(request.REQUEST['dc_user_id'])
    points_awarded = int(request.REQUEST['points_awarded'])
    task = request.REQUEST['task']
    summary = request.REQUEST['summary']
    candidate_code = request.REQUEST['candidate_code']
    candidate_name = request.REQUEST['candidate_name']
    party_name = request.REQUEST['party_name']
    details_added = request.REQUEST['details_added']

    user = None
    try:
        user = CustomUser.objects.get(pk=dc_user_id)
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound()

    if points_awarded != 0:
        ynmp_action = YNMPAction.objects.create(user=user,
                                                points_awarded=points_awarded,
                                                task=task,
                                                summary=summary,
                                                candidate_code=candidate_code,
                                                candidate_name=candidate_name,
                                                party_name=party_name,
                                                details_added=details_added)
        user.points += points_awarded
        user.save()

        ynmp_action_done.send(None, user=user, ynmp_action=ynmp_action)

    json_response = _build_json_response(user)

    return HttpResponse(json_response)

@login_key
@login_required
def start(request):
    import pdb; pdb.set_trace()
    # http://localhost:8008/tasks/ynmp-details/start/523bad3799ed898218d87234f47c8a7c444fb967/
    return HttpResponseRedirect(ynmp_login_url(request.user, "bad_details"))

"""
JSON response looks like

{
>    dc_user_id : 123,
>    total_points: 10,
>    leader_board: [
>      { name: 'Susan', points: 1000, dc_user_id: 89 },
>      ... top ten say ...
>    ]
> }
"""
