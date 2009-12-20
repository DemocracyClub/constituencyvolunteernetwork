from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site

from tasks.models import Task, TaskUser, Badge
from signup.signals import *
from signals import *

from tasks.util import reverse_login_key

task_slug = "upload-leaflet"
tsc_url = "http://www.thestraightchoice.org/addupload.php"

def callback_leaflet_added(sender, **kwargs):
    """
        Automatically set this task as complete if we've sent three or more invitations
        Possibility: Make this only trigger if three friends ACCEPT an invitation?
    """
    user = kwargs['user']

    try:
        task = Task.objects.get(slug=task_slug)
    except Task.DoesNotExist:
        return None

    print "Checking user %s on task %s" % (user, task)

    try:
        task_user = TaskUser.objects.get(task=task,user=user)
    except TaskUser.DoesNotExist:
        return None

    # Only do the task once?
    if task_user.state != 3:
        task_user.complete()
    
    # But give them another badge every time they do it
    badge = Badge.objects.create(name="Uploaded a leaflet", task=task, user=user)
    badge.save()

    print "Completed %s" % task_user

def callback_assign(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and isn't
        already doing the task.
    """
    user = kwargs['user']
    
    try:
        task = Task.objects.get(slug=task_slug)
    except Task.DoesNotExist:
        print "Could not find task %s" % task_slug
        return None
    
    try:
        current_site = Site.objects.get_current()

        post_url = "http://%s%s" % \
               (current_site.domain, reverse_login_key("tsc_add", user))

        TaskUser.objects.assign_task(task, user, tsc_url, post_url)
    except TaskUser.AlreadyAssigned:
        print "%s already assigned to %s" % (task, user)
        pass

# Assignment signals
user_activated.connect(callback_assign)
user_touch.connect(callback_assign)

# Completion signals
leaflet_added.connect(callback_leaflet_added)
