import re

from django.contrib.sites.models import Site

from tasks.models import TaskUser, Badge
from signup.signals import *
from signals import *

from tasks.util import reverse_login_key
from tasks.decorators import task_assign, task_completion

task_slug = "upload-leaflet"
#tsc_url = "http://www.thestraightchoice.org/addupload.php"
tsc_url = "/tsc/test"

@task_completion(task_slug)
def callback_leaflet_added(sender, **kwargs):
    """
        Automatically set this task as complete when we add a leaflet
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']
    
    # Only do the task once?
    if task_user.state != TaskUser.States.completed:
        task_user.complete()
    
    # But upgrade their badge every time they do it
    try:
        badge = Badge.objects.get(task=task, user=user)
        badge.number += 1
        badge.save()
    except Badge.DoesNotExist:
        badge = Badge.objects.create(name="Uploaded a leaflet",
                                     task=task,
                                     user=user)

@task_assign(task_slug)
def callback_assign(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and
        isn't already doing the task.
    """
    user = kwargs['user']
    task = kwargs['task']
    current_site = Site.objects.get_current()
    post_url = "http://%s%s" % \
        (current_site.domain, reverse_login_key("tsc_add", user)) 
    try:
        TaskUser.objects.assign_task(task,
                                     user,
                                     tsc_url,
                                     post_url=post_url,
                                     email=True)
    except TaskUser.AlreadyAssigned:
        return "%s already assigned to %s" % (task, user)

# Assignment signals
# user_activated.connect(callback_assign)
user_touch.connect(callback_assign)

# Completion signals
leaflet_added.connect(callback_leaflet_added)

