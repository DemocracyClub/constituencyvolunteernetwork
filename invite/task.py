from tasks.rules import ViewPathAssignToAll
from django.core.urlresolvers import reverse

invite_task = ViewPathAssignToAll("invite-three-friends", "inviteindex")
