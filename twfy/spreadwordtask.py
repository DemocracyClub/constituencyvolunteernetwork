from tasks.models import TaskUser, Badge
from signup.signals import *

from tasks.decorators import task_assign, task_completion

task_slug = "spread-word"

@task_completion(task_slug)
def callback_spread_done(sender, **kwargs):
    """
        Set this task as complete when some hassling has been done
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']
    
    if task_user.state != TaskUser.States.completed:
        task_user.complete()
    
    try:
        badge = Badge.objects.get(task=task, user=user)
        badge.number += 1
        badge.save()
    except Badge.DoesNotExist:
        badge = Badge.objects.create(name="Spread the word",
                                     task=task,
                                     user=user)

@task_assign(task_slug)
def callback_assign(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and isn't
        already doing the task.
    """
    user = kwargs['user']
    task = kwargs['task']
    constituency = user.home_constituency
    if getattr(constituency,
               'name',
               "no constituency") == "no constituency":
        return "No constituency for %s, not assigning" % user
    slug = user.home_constituency.slug
    url = "http://www.mysociety.org/2010/05/04/how-to-get-theyworkforyou-into-your-local-paperradio-station-in-5-minutes/"
    msg = ""
    try:                
        TaskUser.objects.assign_task(task,
                                     user,
                                     url)
    except TaskUser.AlreadyAssigned:
        msg = "%s already assigned to %s" % (task, user)
    return msg

# Assignment signals
user_activated.connect(callback_assign)
user_touch.connect(callback_assign)
