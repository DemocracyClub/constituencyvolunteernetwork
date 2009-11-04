from django.core.urlresolvers import reverse

from tasks.models import Task, TaskUser
from signup.signals import *

def callback_assign(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and isn't
        already doing the task.
    """
    user = kwargs['user']
    
    try:
        task = Task.objects.get(slug="invite-three-friends")
    except Task.DoesNotExist:
        return
    
    try:
        TaskUser.objects.assign_task(task, user, reverse("inviteindex"))
    except TaskUser.AlreadyAssigned:
        # print "%s already assigned to %s" % (task, user)
        pass
        
#user_join.connect(callback_assign)
#user_touch.connect(callback_assign)
