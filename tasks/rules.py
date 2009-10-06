"""
    Factory functions for pre-made rules for assigning tasks.
"""
from signup.signals import *
from signup.models import Constituency
from models import Task, TaskUser
    
class Rule:
    def __init__(self):
        self.register()

    def register(self):
        pass

class AssignToAll(Rule):
    def __init__(self, task_slug, url_pattern):
        Rule.__init__(self)
        self.task = Task.objects.get(slug=task_slug)
        self.url_pattern = url_pattern

    def register(self):
        user_join.connect(self.callback_assign)
        user_touch.connect(self.callback_assign)
    
    def callback_assign(self, sender, **kwargs):
        self.user = kwargs['user']
        
        try: # Make sure we're not already assigned this task, unless we want to
             # somehow assign a task multiple times for different constituencies?
            TaskUser.objects.get(user=self.user, task=self.task)
        except TaskUser.DoesNotExist:
            TaskUser.objects.assign_task(task, user, self.url())
    
    def url(self):
        return self.url_pattern % self.user.id

class AssignToConstituency(Rule):
    def __init__(self, task_slug, constituency_slug, url_pattern):
        Rule.__init__(self)
        self.task = Task.objects.get(slug=task_slug) # Bit of an overhead always loading these objects? Just store slugs?
        self.constituency = Constituency.objects.get(slug=constituency_slug)
        self.url_pattern = url_pattern
    
    def register(self):
        user_join.connect(self.callback_assign)
        user_join_constituency.connect(self.callback_assign)
        user_touch.connect(self.callback_assign)
    
    def callback_assign(self, sender, **kwargs):
        self.user = kwargs['user']
        
        # Either we know the constituency and we can check it, or we check to see
        # if the user is a member of the constituency
        if ('constituency' in kwargs and kwargs['constituency'] == self.constituency) or (self.user.constituencies.filter(pk=self.constituency.id)):
            try: # Already on this task?
                TaskUser.objects.get(user=self.user, task=self.task)
            except TaskUser.DoesNotExist:
                TaskUser.objects.assign_task(self.task, self.user, self.url())
    
    def url(self):
        return self.url_pattern % self.user.id