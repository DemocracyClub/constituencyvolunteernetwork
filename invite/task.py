from tasks.rules import AssignToAll
from django.core.urlresolvers import reverse

class InviteAssignToAll(AssignToAll):
    def url(self):
        return reverse(self.url_pattern)

invite_task = InviteAssignToAll("invite-three-friends", "inviteindex")
