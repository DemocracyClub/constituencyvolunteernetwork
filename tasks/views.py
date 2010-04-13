import os

import datetime

from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.http import urlquote
from django.shortcuts import get_object_or_404

from models import Task, TaskUser, TaskEmailUser
from models import TaskEmail
from models import Badge
from signup.models import CustomUser, Constituency
from signup.views import render_with_context
from signup.views import _get_statistics_context
from signup.signals import user_touch
from tasks.util import login_key
from tasks.activity import generate_activity

import settings

SPACER_GIF = open(
    os.path.join(settings.MEDIA_ROOT, "spacer.gif"), "rb"
    ).read()

@login_required
def home(request):
    context = _get_statistics_context()        

    tasks = TaskUser.objects.filter(
            user=request.user).order_by('state', 'date_assigned')
    open_tasks = tasks.filter(state__in=[TaskUser.States.started,
                                         TaskUser.States.assigned,
                                         TaskUser.States.ignored])
    completed_tasks = tasks.filter(state=TaskUser.States.completed)
    ignored_tasks = tasks.filter(state=TaskUser.States.ignored)
    context['all_tasks'] = tasks
    context['open_tasks'] = open_tasks
    context['completed_tasks'] = completed_tasks
    context['ignored_tasks'] = ignored_tasks
    context['badges'] = Badge.objects.filter(user=request.user)
    context['new_signups'] = CustomUser.objects\
                             .order_by('-date_joined')[:5]
    context['first_time'] = request.user.login_count < 3
    constituencies = request.user.constituencies.all()
    context['activity'] = generate_activity(constituencies)
    
    return render_with_context(request, 'tasks/tasks.html', context)

@login_key
def task(request, slug, constituency=None):
    """
        Check out a task. Needs to also optionally take a login token to allow
        direct access to the task by email.
    """
    context = {}
    context['task'] = Task.objects.get(slug=slug)

    if constituency is not None:
        year = settings.CONSTITUENCY_YEAR
        c = Constituency.objects.get(slug=constituency,
                                     year=year)
        context['constituency'] = Constituency.objects\
                                  .get(slug=constituency,
                                       year=year)
    else:
        context['constituency'] = None;
    
    if request.user.is_authenticated():
        items = TaskUser.objects
        
        if constituency is not None:
            try:
                context['usertasks'] = [items.get(task=context['task'],
                                                user=request.user,
                                                constituency=context['constituency'])]
            except TaskUser.DoesNotExist:
                pass
        else: # For the root task page, list all constituencies
            context['usertasks'] = items.filter(task=context['task'],
                                                user=request.user)
    else:
        context['usertasks'] = None

    started_tu = TaskUser.objects.filter(task=context['task'],\
                                         state=TaskUser.States.started)
    if constituency is not None:
        started_tu = started_tu.filter(constituency=context['constituency'])
    
    context['started_users'] = \
        CustomUser.objects.filter(taskuser__in=started_tu).distinct()
    
    return render_with_context(request, 'tasks/task_page.html', context)

@login_key
@login_required
def start_task(request, slug, constituency=None):
    """
        Mark this task as started by this user,then redirect the user to
        the task url
    """
    task = Task.objects.get(slug=slug)
    try:
        task_user = TaskUser.objects.get(task=task,
                                         user=request.user,
                                         constituency__slug=constituency)
        task_user.start()
        url = task_user.url
        if task_user.post_url:
            url += "?callback=" + urlquote(task_user.post_url)
        return HttpResponseRedirect(url)
    except TaskUser.DoesNotExist:
        raise Http404("Task user does not exist for task '%s', user '%s', constituency '%s'" % (task, request.user, constituency))

@login_key
@login_required
def ignore_task(request, slug, constituency=None):
    """
        Ignore the task then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug,
                                     user=request.user,
                                     constituency__slug=constituency)
    task_user.ignore()
    
    return HttpResponseRedirect(reverse("tasks"))

@login_required
def unignore_task(request, slug, constituency=None):
    """
        Unignore the task then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug,
                                     user=request.user,
                                     constituency__slug=constituency)
    task_user.state = 0
    task_user.save()
    
    return HttpResponseRedirect(reverse("task", args={slug: slug}))

@login_key
@login_required
def complete_task(request, slug, constituency=None):
    """
        Mark the task as complete then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug,
                                     user=request.user,
                                     constituency__slug=constituency)
    task_user.complete()
    if task_user.post_url:
        return HttpResponseRedirect(task_user.post_url)
    else:
        return HttpResponseRedirect(reverse("tasks"))

@login_required
@permission_required('tasks.add_taskuser')
def admin_assign_all(request):
    from forms import AssignForm
    from signup.models import CustomUser
    
    context = {}

    if request.method == "POST":
        form = AssignForm(request.POST, request.FILES)
        if form.is_valid():
            all_users = CustomUser.objects.filter(
                is_active=True)
            context['message'] = []
            for task in form.cleaned_data['tasks']:
                (assigned, already_assigned) = TaskUser.objects.trigger_assign(task, all_users)
                context['message'].append((task, assigned, already_assigned))
                
            context['form'] = form
        else:
            context['form'] = form
    else:
        context['form'] = AssignForm()
    
    return render_with_context(request, 'tasks/task_admin.html', context)

@login_required
@permission_required('tasks.add_taskuser')
def admin_assign_constituency(request):
    from forms import AssignConstituency
    from signup.models import CustomUser
    
    context = {}

    if request.method == "POST":
        form = AssignConstituency(request.POST, request.FILES)
        if form.is_valid():
            constituencies = form.cleaned_data['constituencies']
            all_users = CustomUser.objects.filter(
                is_active=True,
                constituencies__in=constituencies)
            
            context['message'] = []
            for task in form.cleaned_data['tasks']:
                (assigned, already_assigned) = TaskUser.objects.trigger_assign(task, all_users, constituencies)
                task_string = "%s in %s" % (task, constituencies)
                context['message'].append((task_string, assigned, already_assigned))
            
            context['form'] = form
        else:
            context['form'] = form
    else:
        context['form'] = AssignConstituency()
    
    return render_with_context(request, 'tasks/task_admin.html', context)


@login_required
@permission_required('tasks.add_taskuser')
def manage_tasks(request):
    tasks = Task.objects.all()
    context= {}
    context['tasks'] = tasks
    return render_with_context(request,
                               'tasks/manage_tasks.html',
                               context) 

@login_required
@permission_required('tasks.add_taskuser')
def manage_assign_tasks(request, task_pk):
    context = {}
    task = get_object_or_404(Task, pk=task_pk)
    context['task'] = task
    dry_run = False
    count = 0
    skip = 0
    matched_users = []
    email = None
    
    if request.method == "POST":
        dry_run = request.POST.get('dry_run', False)
        queryfilter = request.POST['queryfilter'].strip()
        users = CustomUser.objects.all()
        
        if queryfilter:
            users = eval(queryfilter.strip())

        users = users.filter(is_active=True, unsubscribed=False) # enforce
        
        for user in users:
            matched_users.append(user.email)

            if TaskUser.objects.filter(user=user,
                                       task__pk=task_pk): # Already assigned
                skip += 1
                continue
            else:
                if not dry_run:
                    # Trigger assignment
                    responses = user_touch.send(None,
                                                user=user,
                                                task_slug=task.slug)
                count += 1
        
        context['posted'] = True
        context['queryfilter'] = queryfilter
        context['matched_users'] = matched_users
    
    context['emails'] = TaskEmail.objects\
                        .distinct()\
                        .order_by("-date_created")
    context['dry_run'] = dry_run
    context['count'] = count
    context['skip'] = skip
    context['selected_email'] = email
    return render_with_context(request,
                               'tasks/manage_assign_tasks.html',
                               context)

@login_required
@permission_required('tasks.add_taskuser')
def manage_assign_email(request, task_pk):
    """
        Assign an email to be sent for particular users.
        Creates TaskEmailUser objects to represent assignment
    """
    context = {}
    matched_users = []
    count = 0
    skip = 0
    task = get_object_or_404(Task, pk=task_pk)
    dry_run = request.POST.get('dry_run', False)
    selected_email = request.POST.get('email', None)

    email = None
    if selected_email:
        email = TaskEmail.objects.get(pk=selected_email)
    
    if request.method == "POST":
        queryfilter = request.POST['queryfilter'].strip()      
        users = CustomUser.objects.all()
        
        if queryfilter:
            users = eval(queryfilter.strip())

        users = users.filter(is_active=True, unsubscribed=False) # enforce
        
        for user in users:
            matched_users.append(user.email)
            taskusers = TaskUser.objects.filter(user=user,
                                                task=task)
            for task_user in taskusers:
                try:
                    task_email_user = TaskEmailUser.objects.get(task_email=email,
                                                                task_user=task_user)
                except TaskEmailUser.DoesNotExist:
                    if not dry_run:
                        task_email_user = TaskEmailUser.objects.create(task_email=email,
                                                                       task_user=task_user)        
                    count += 1
        
        context['posted'] = True
        context['matched_users'] = matched_users        
        context['queryfilter'] = queryfilter

    context['task'] = task
    context['emails'] = TaskEmail.objects.filter(task=task) \
                                         .order_by("-date_created")
    context['dry_run'] = dry_run
    context['count'] = count
    context['skip'] = skip
    context['selected_email'] = email
    return render_with_context(request,
                               'tasks/manage_assign_email.html',
                               context)

def scan_queue(request, dry_run=False):
    # Look at the email queue, determine if there are any emails which can be sent
    users = CustomUser.objects.all()
    
    context = {}
    sent = []
    for user in users:
        emails = TaskEmailUser.objects.filter(task_user__user=user).distinct()

        # Find out what the date was for the last sending
        last_sent = emails.exclude(date_sent=None).order_by('-date_added')
        date_last_sent = None
        if last_sent:
            date_last_sent = last_sent[0].date_sent
        
        # Only email once every two days
        if date_last_sent and date_last_sent > datetime.datetime.now() - datetime.timedelta(2):
            continue
        
        # Send unsent once-off messages with priority, then look for reminders
        # that are more than a week since they were last sent
        oldest_unsent = emails.filter(date_sent=None,
                                      task_email__email_type__in=[TaskEmail.EmailTypes.welcome,
                                                                  TaskEmail.EmailTypes.oneoff,],
                                     ).order_by('date_added')
        
        send_task_email_user = None
        if oldest_unsent:
            send_task_email_user = oldest_unsent[0]
        else:
            week_ago = datetime.datetime.now() - datetime.timedelta(7)

            # Find unsent reminders first
            reminders = emails.filter(date_sent=None,
                                      task_email__email_type=TaskEmail.EmailTypes.reminder
                                     ).order_by('date_sent')

            # If we cant find unsent reminders, find the oldest reminder sent more than a week ago
            if not reminders:
                reminders = emails.filter(date_sent__lte=week_ago,
                                          task_email__email_type=TaskEmail.EmailTypes.reminder
                                         ).order_by('date_sent')

            if reminders:
                send_task_email_user = reminders[0]

        if send_task_email_user:
            if not dry_run:
                success = send_task_email_user.send()
                if success:
                    sent.append(send_task_email_user)
            else:
                sent.append(send_task_email_user)
    
    context['sent'] = sent
    context['dry_run'] = dry_run

    return render_with_context(request,
                               'tasks/emails_sent.html',
                               context)

def open_email(request, taskuser_id, taskemail_id):
    """
    Mark a TaskUser as having had an email opened and return a gif 
    """
    try:
        task_user = TaskUser.objects.get(pk=taskuser_id)
        task_email = TaskEmail.objects.get(pk=taskemail_id)
        task_user.source_email = task_email
        task_user.save()
        task_email.opened += 1
        task_email.save()
        return HttpResponse(content=SPACER_GIF,
                            mimetype="image/gif")
    except TaskUser.DoesNotExist:
        raise Http404()

#26;"signup";"0004_points_field";"2010-03-16 23:20:08.438685+00"
    
