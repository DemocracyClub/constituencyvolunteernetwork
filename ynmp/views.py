try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotFound, HttpResponseRedirect

from signup.models import CustomUser

from models import YNMPAction
from signals import ynmp_action_done
from util import ynmp_login_url

def _build_leader_board():
    users = CustomUser.objects.order_by('-points')[0:5]

    leader_board = []
    for user in users:
        leader_board.append({'name': user.display_name,
                             'points': user.points,
                             'dc_user_id': user.id})

    return leader_board

def _build_json_response(user):
    response = {}
    response['dc_user_id'] = user.id
    response['total_points'] = user.points
    response['leader_board'] = _build_leader_board()

    return json.dumps(response)

def api(request):
    if 'dc_user_id' not in request.REQUEST or 'points_awarded' not in request.REQUEST:
        return HttpResponseBadRequest()

    dc_user_id = int(request.REQUEST['dc_user_id'])
    points_awarded = int(request.REQUEST['points_awarded'])
    task = str(request.REQUEST['task'])
    summary = str(request.REQUEST['summary'])

    user = None
    try:
        user = CustomUser.objects.get(pk=dc_user_id)
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound()

    if points_awarded != 0:
        ynmp_action = YNMPAction.objects.create(user=user,
                                                points_awarded=points_awarded,
                                                task=task,
                                                summary=summary)
        user.points += points_awarded
        user.save()

        ynmp_action_done.send(None, kwargs={'user':user, 'ynmp_action':ynmp_action})

    json_response = _build_json_response(user)

    return HttpResponse(json_response)

def start(request):
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
