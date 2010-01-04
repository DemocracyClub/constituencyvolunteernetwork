from django.core.urlresolvers import reverse

from models import Invitation
from tasks.models import Task, TaskUser, Badge
from signup.signals import *
from invite.signals import *

from tasks.decorators import task_assign, task_completion

@task_completion("invite-three-friends")
def callback_invites_sent(sender, **kwargs):
    """
        Automatically set this task as complete if we've sent three or more invitations
        Possibility: Make this only trigger if three friends ACCEPT an invitation?
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']
    
    if Invitation.objects.filter(user_from=user).count() > 2:
        task_user.complete()
        badge = Badge.objects.create(name="Invited three friends", task=task, user=user)

        print "Completed %s" % task_user

@task_assign("invite-three-friends")
def callback_assign(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and isn't
        already doing the task.
    """
    user = kwargs['user']
    task = kwargs['task']
    
    #try:
    TaskUser.objects.assign_task(task, user, reverse("inviteindex"), False)
    #except TaskUser.AlreadyAssigned:
    #    print "%s already assigned to %s" % (task, user)
    #    pass

# Assignment signals
user_activated.connect(callback_assign)
user_touch.connect(callback_assign)

# Completion signals
invitation_sent.connect(callback_invites_sent)
user_touch.connect(callback_invites_sent)
