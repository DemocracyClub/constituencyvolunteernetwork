import re

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from tasks.models import TaskUser, Badge
from signup.signals import *

from tasks.decorators import task_assign, task_completion

from signals import *
import util

task_slug = "ynmp-details"

@task_completion(task_slug)
def callback_ynmp_done(sender, **kwargs):
    """
        Set this task as complete when some sufficient amount of ynmp work is done
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']
    ynmp_action = kwargs['ynmp_action']
    
    if task_user.state != TaskUser.States.completed:
        task_user.complete()
    
    try:
        badge = Badge.objects.get(task=task, user=user)
        badge.number += 1
        badge.save()
    except Badge.DoesNotExist:
        badge = Badge.objects.create(name="Added details on YNMP",
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
    url = ynmp_login_url(user, "bad_details")
    try:                
        TaskUser.objects.assign_task(task,
                                     user,
                                     url)
    except TaskUser.AlreadyAssigned:
        msg = "%s already assigned to %s" % (task, user)
    return msg

# Assignment signals
# user_activated.connect(callback_assign)
user_touch.connect(callback_assign)

# Completion signals
interest_expressed.connect(callback_interest_expressed)

