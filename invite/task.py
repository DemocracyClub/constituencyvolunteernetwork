from django.core.urlresolvers import reverse

from models import Invitation
from tasks.models import Task, TaskUser
from signup.signals import *
from invite.signals import *

def callback_invites_sent(sender, **kwargs):
    """
        Automatically set this task as complete if we've sent three or more invitations
        Possibility: Make this only trigger if three friends ACCEPT an invitation?
    """
    user = kwargs['user']
    task = Task.objects.get(slug="invite-three-friends")

    print "Checking user %s on task %s" % (user, task)

    if Invitation.objects.filter(user_from=user).count() > 2:
        task_user = TaskUser.objects.get(task=task,user=user)
        task_user.complete()

        print "Completed %s" % task_user

def callback_assign(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and isn't
        already doing the task.
    """
    user = kwargs['user']
    
    try:
        task = Task.objects.get(slug="invite-three-friends")
    except Task.DoesNotExist:
        return None
    
    try:
        TaskUser.objects.assign_task(task, user, reverse("inviteindex"))
    except TaskUser.AlreadyAssigned:
        print "%s already assigned to %s" % (task, user)
        pass

# Assignment signals
#user_join.connect(callback_assign)
#user_touch.connect(callback_assign)

# Completion signals
#invitation_sent.connect(callback_invites_sent)
#user_touch.connect(callback_invites_sent)
