import re

from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse

from tasks.models import TaskUser, Badge
from signup.signals import *
from signals import *

from tasks.decorators import task_assign, task_completion

task_slug = "organise-meeting"

@task_completion(task_slug)
def callback_interest_expressed(sender, **kwargs):
    """
        Automatically set this task as complete when we add a leaflet
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']
    
    # Only do the task once?
    if task_user.state != TaskUser.States.completed:
        task_user.complete()
        try:
            badge = Badge.objects.get(task=task, user=user)
            badge.number += 1
            badge.save()
        except Badge.DoesNotExist:
            badge = Badge.objects.create(name="Attended a local meeting",
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
    msg = ""
    express_interest_url = reverse("express_interest")
    try:                
        TaskUser.objects.assign_task(task,
                                     user,
                                     express_interest_url)
    except TaskUser.AlreadyAssigned:
        msg = "%s already assigned to %s" % (task, user)
    return msg

# Assignment signals
#user_activated.connect(callback_assign)
user_touch.connect(callback_assign)

# Completion signals
interest_expressed.connect(callback_interest_expressed)

