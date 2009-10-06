from tasks.rules import TaskRouterAssignAll
from django.core.urlresolvers import reverse

class InviteTask(TaskRouterAssignAll):
    task_slug = "invite-three-friends"
    
    def url(self, user):
        return reverse("inviteindex")
        
invite_task = InviteTask()
