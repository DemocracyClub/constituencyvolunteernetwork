from django.template.loader import render_to_string

from comments_custom.models import CommentSimple

def generate_activity(constituencies, **kwargs):
    from models import Task, TaskUser
    if constituencies:
        # the strange way we construct the query with "__id__in"
        # operators is necessary because otherwise we get
        # subquery-related complaints from postgres
        ids = [x.id for x in constituencies]

        show_constituency = True
        if 'show_constituency' in kwargs:
            show_constituency = kwargs['show_constituency']
        
        # Pull out activity for people doing tasks
        task_users = TaskUser.objects\
          .filter(user__constituencies__id__in=ids)\
          .filter(state__in=[TaskUser.States.started,
                            TaskUser.States.completed])\
          .order_by('-date_modified').distinct().all()

        task_user_activity = [(task_user.date_modified,
                                 render_to_string('tasks/activity_task_user.html',
                                                 {'item': task_user,
                                                  'show_constituency': show_constituency,}),
                              ) for task_user in task_users]
    
        # Pull out activity for people posting comments
        comments = CommentSimple.objects\
          .filter(object_pk__in=[str(id) for id in ids])\
          .order_by('-submit_date').distinct().all()

        comments_activity = [(comment.submit_date,
                                 render_to_string('tasks/activity_comment.html',
                                                 {'comment': comment,
                                                  'show_constituency': show_constituency,}),
                              ) for comment in comments]
        
        # Combine the two, sorted by date, and get rid of the date
        return [x[1] for x in sorted(task_user_activity + comments_activity, reverse=True)]
