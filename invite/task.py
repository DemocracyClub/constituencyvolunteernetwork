from django.core.urlresolvers import reverse

from models import Invitation
from tasks.models import Task, TaskUser, Badge
from signup.signals import *
from invite.signals import *

from tasks.decorators import task_assign, task_completion

award_levels  = {3: 'three', 10: 'ten', 20: 'twenty',
                 50: 'fifty', 100: 'one hundred',}

task_slug = "invite-three-friends"

@task_completion(task_slug)
def callback_invites_sent(sender, **kwargs):
    """
        Automatically set this task as complete if we've sent three or more invitations
        Possibility: Make this only trigger if three friends ACCEPT an invitation?
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']

    invite_count = Invitation.objects.filter(user_from=user).count()
    
    if invite_count > 2:
        if task_user.state != TaskUser.States.completed:
            task_user.complete()
    
    # Only award the badge at particular stages. Bit messy, but has to work
    # for users with existing invites and for bulk invites
    for level, text in sorted(award_levels.items()):
        if invite_count >= level:
            if not Badge.objects.filter(name="Invited %s friends" % text,\
                                        user=user):
                badge = Badge.objects.create(name="Invited %s friends" %\
                                                   text,
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
    try:
        TaskUser.objects.assign_task(task, user, reverse("inviteindex"))
    except TaskUser.AlreadyAssigned:
        return "%s already assigned to %s" % (task, user)

# Assignment signals
user_activated.connect(callback_assign)
user_touch.connect(callback_assign)

# Completion signals
invitation_sent.connect(callback_invites_sent)
user_touch.connect(callback_invites_sent)
