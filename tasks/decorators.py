from tasks.models import Task

def task_assign(task_slug):
    """
        Decorator for task assignment callbacks
        Adds code to automatically load in the task object, and to filter out
        signals that are targeted at a specific task
    """
    try:
        task = Task.objects.get(slug=task_slug)
    except Task.DoesNotExist:
        # If the task doesn't exist, return a dud callback
        print "Task \"%s\" doesn't exist while generating callback" % task_slug
        def _task_assign(callback):
            def _callback(sender, **kwargs):
                return None
            return _callback
        return _task_assign

    def _task_assign(callback):
        # New callback function
        def _callback(sender, **kwargs):
            # Allow signals to invoke a particular task
            if 'task_slug' in kwargs and kwargs['task_slug'] != None\
                    and kwargs['task_slug'] != task_slug:
                return None

            kwargs['task'] = task # inject our task object
            return callback(sender, **kwargs)
        return _callback
    return _task_assign