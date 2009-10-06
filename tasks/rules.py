"""
    Task routers handle the signals that affect tasks. They can assign tasks to
    users based on signals, and they can change the state of a usertask based on
    signals.
"""
from signup.signals import *
from signup.models import Constituency
from models import Task, TaskUser
from django.core.urlresolvers import reverse

task_completed = django.dispatch.Signal(providing_args=["user", "task_slug"])

class TaskRouter:
    def __init__(self):
        self.task = Task.objects.get(slug=self.task_slug)
        self.register()

    def register(self):
        """
            Register signal callbacks.
        """
        task_completed.connect(self.callback_completed)  # Activated on task completion
        
    def callback_completed(self, sender, **kwargs):
        """
            Allows task code to declare that a user has completed a task
        """
        task_slug = kwargs['task_slug']
        
        if task_slug == self.task_slug:
            task_user = TaskUser.objects.get(task__slug=task_slug, user=kwargs['user'])
            task_user.complete()

class TaskRouterAssignAll(TaskRouter):
    def __init__(self):
        TaskRouter.__init__(self)

    def register(self):
        user_join.connect(self.callback_assign)
        user_touch.connect(self.callback_assign)
        task_completed.connect(self.callback_completed)

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

class TaskRouterAssignConstituency(TaskRouter):
    """
        Assign this task to everyone in or joining this constituency
    """
    def __init__(self):
        TaskRouter.__init__(self)
        self.constituency = Task.objects.get(slug=self.constituency_slug)
    
    def register(self):
        user_join.connect(self.callback_assign)
        user_join_constituency.connect(self.callback_assign)
        user_touch.connect(self.callback_assign)
        task_completed.connect(self.callback_completed)
    
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
        return self.url_pattern % user.id