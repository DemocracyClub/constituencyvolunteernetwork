try:
    import json
except ImportError:
    import simplejson as json

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound

from signup.models import CustomUser

from models import YNMPAction
from signals import ynmp_action_done

def _build_leader_board():
    return [{ 'name': 'Susan', 'points': 1000, 'dc_user_id': 89 },]

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
    summary_of_task = str(request.REQUEST['summary_of_task'])

    user = None
    try:
        user = CustomUser.objects.get(pk=dc_user_id)
    except CustomUser.DoesNotExist:
        return HttpResponseNotFound()
    
    if points_awarded != 0:
        ynmp_action = YNMPAction.objects.create(user=user,
                                                points_awarded=points_awarded,
                                                task=task,
                                                summary_of_task=summary_of_task)
        user.points += points_awarded
        user.save()

        ynmp_action_done.send(user=user, ynmp_action=ynmp_action)
    
    json_response = _build_json_response(user)
    return HttpResponse(json_response)

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
