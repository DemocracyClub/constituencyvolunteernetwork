from tasks.models import Task, TaskUser

def task_assign(task_slug):
    """
        Decorator for task assignment callbacks
        Adds code to automatically load in the task object, and to filter out
        signals that are targeted at a specific task
    """
    def _task_assign(callback):
        # New callback function
        def _callback(sender, **kwargs):
            # Allow signals to invoke a particular task
            if 'task_slug' in kwargs and kwargs['task_slug'] != None\
                    and kwargs['task_slug'] != task_slug:
                return None
            
            task = Task.objects.get(slug=task_slug)
            
            kwargs['task'] = task # inject our task object
            result = callback(sender, **kwargs)
            if result:
                return result
            else:
                return "Assigned %s" % task_slug
    
        return _callback
    return _task_assign

def task_completion(task_slug):
    """
        Decorator for task completion callbacks. Pulls in task object
        and taskuser obejct.
    """
    def _task_completion(callback):
        def _callback(sender, **kwargs):
            # Allow signals to invoke a particular task
            if 'task_slug' in kwargs and kwargs['task_slug'] != None\
                    and kwargs['task_slug'] != task_slug:
                return None
            
            user = kwargs['user']
            constituency = kwargs.get('constituency', None)
            try:
                kwargs['task'] = Task.objects.get(slug=task_slug)
            except Task.DoesNotExist:
                return None

            print "Checking user %s on task %s" % (user, kwargs['task'])

            try:
                items = TaskUser.objects
                kwargs['task_user'] = items.get(task=kwargs['task'],
                                                user=user,
                                                constituency=constituency)
            except TaskUser.DoesNotExist:
                return None

            return callback(sender, **kwargs)

        return _callback
    return _task_completion
