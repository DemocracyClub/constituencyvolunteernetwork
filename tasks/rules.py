"""
    Old code for rules. The Invite example currently does this itself.
"""
from signup.signals import *
from signup.models import Constituency
from models import Task, TaskUser
from django.core.urlresolvers import reverse

class TaskRouter:
    def __init__(self, task_slug, url_pattern):
        self.task_slug = task_slug
        self.url_pattern = url_pattern
        self.task = Task.objects.get(slug=self.task_slug)
        self.register_callbacks()

    def register_callbacks(self):
        """
            Register signal callbacks.
        """
        pass

class TaskRouterAssignAll(TaskRouter):
    def __init__(self, task_slug, url_pattern):
        TaskRouter.__init__(self, task_slug, url_pattern)

    def register_callbacks(self):
        user_join.connect(self.callback_assign)
        user_touch.connect(self.callback_assign)

    def callback_assign(self, sender, **kwargs):
        """
            Assign this task to everyone who activates the signals and isn't
            already doing the task.
        """
        user = kwargs['user']
        
        try: # Make sure we're not already assigned this task, unless we want to
             # somehow assign a task multiple times for different constituencies?
            TaskUser.objects.get(user=user, task=self.task)
        except TaskUser.DoesNotExist:
            TaskUser.objects.assign_task(self.task, user, self.url(user))
            
    def url(self, user):
        return reverse(self.url_pattern)

class TaskRouterAssignConstituency(TaskRouter):
    """
        Assign this task to everyone in or joining this constituency
    """
    def __init__(self, constituency_slug, task_slug, url_pattern):
        TaskRouter.__init__(self, task_slug, url_pattern)
        self.constituency_slug = constituency_slug
        self.constituency = Task.objects.get(slug=self.constituency_slug)
    
    def register_callbacks(self):
        user_join.connect(self.callback_assign)
        user_join_constituency.connect(self.callback_assign)
        user_touch.connect(self.callback_assign)
    
    def callback_assign(self, sender, **kwargs):
        user = kwargs['user']
        
        # Either we know the constituency and we can check it, or we check to see
        # if the user is a member of the constituency
        if ('constituency' in kwargs and kwargs['constituency'] == self.constituency) or (self.user.constituencies.filter(pk=self.constituency.id)):
            try: # Already on this task?
                TaskUser.objects.get(user=user, task=self.task)
            except TaskUser.DoesNotExist:
                TaskUser.objects.assign_task(self.task, user, self.url(user))
    
    def url(self, user):
        return reverse(self.url_pattern)
        
routers = {'assign_all': TaskRouterAssignAll, 'assign_constituency': TaskRouterAssignConstituency}
