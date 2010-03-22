from django.template.loader import render_to_string

from comments_custom.models import CommentSimple

def generate_activity(constituencies, **kwargs):
    from models import Task, TaskUser
    from issue.models import Issue
    from tsc.models import UploadedLeaflet
    from ynmp.models import YNMPAction
    
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

        # Pull out activity for people posting issues
        issues = Issue.objects.filter(constituency__id__in=ids)\
                              .order_by('-created_at').distinct().all()

        issues_activity = [(issue.created_at,
                            render_to_string('tasks/activity_issue.html',
                                             {'issue': issue,
                                              'show_constituency': show_constituency,}),
                           ) for issue in issues]

        # Activity for people posting leaflets
        leaflets = UploadedLeaflet.objects.filter(constituency__id__in=ids)\
                                  .order_by('-date').distinct().all()

        leaflets_activity = [(leaflet.date,
                            render_to_string('tasks/activity_leaflet.html',
                                             {'leaflet': leaflet,
                                              'show_constituency': show_constituency,}),
                            ) for leaflet in leaflets]

        # Activity for people on YNMP
        ynmp_actions = YNMPAction.objects.filter(user__constituencies__id__in=ids)\
                                         .order_by('-date').distinct().all()
        
        ynmp_activity = [(ynmp_action.date,
                          render_to_string('tasks/activity_ynmp.html',
                                           {'ynmp_action': ynmp_action,}),
                          ) for ynmp_action in ynmp_actions]
        
        # Combine them all, sorted by date, and get rid of the date and cut to 10
        return [x[1] for x in sorted(task_user_activity + \
                                     comments_activity + \
                                     issues_activity + \
                                     leaflets_activity + \
                                     ynmp_activity, reverse=True)][0:10]
