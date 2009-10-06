"""
    Factory functions for pre-made rules for assigning tasks.
"""
from signup.signals import *
from models import Task, TaskUser

def assign_to_all(task_slug, url_template):
    """
        Assign this task to everyone currently on the site and everyone who joins
    """
    # Activated indiscriminately, joining a constituency or by a touch
    def callback_assign(sender, **kwargs):
        # print "Signal received %s" % kwargs['user']
        user = kwargs['user']
        task = Task.objects.get(slug=task_slug)
        
        try: # Make sure we're not already assigned this task, unless we want to
             # somehow assign a task multiple times for different constituencies?
            TaskUser.objects.get(user=user, task=task)
        except TaskUser.DoesNotExist:
            url = url_template % user.email
            TaskUser.objects.assign_task(task, user, url)
    
    user_join.connect(callback_assign)
    user_touch.connect(callback_assign)
    
    return callback_assign
    
def assign_to_constituency(task_slug, url_template, constituency_slug):
    """
        Assign this task to everyone in or joining a particular constituency
    """
    def callback_assign(sender, **kwargs):
        # print "Signal received %s" % kwargs['user']
        user = kwargs['user']
        
        # Either we know the constituency and we can check it, or we check to see
        # if the user is a member of the constituency
        if ('constituency' in kwargs and kwargs['constituency'].slug == constituency_slug) or (user.constituencies.filter(slug=constituency_slug)):
            task = Task.objects.get(slug=task_slug)
            
            try: # Already on this task?
                TaskUser.objects.get(user=user, task=task)
            except TaskUser.DoesNotExist:
                url = url_template % user.email
                TaskUser.objects.assign_task(task, user, url)
    
    user_join.connect(callback_assign)
    user_join_constituency.connect(callback_assign)
    user_touch.connect(callback_assign)
    
    return callback_assign