import os

from django.http import HttpResponseRedirect
from django.http import Http404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.http import urlquote
from django.db.models import Sum
from django.shortcuts import get_object_or_404

from models import Task, TaskUser
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
    selected_email = request.POST.get('email', None)
    email = None
    if request.method == "POST":
        context['posted'] = True
        dry_run = request.POST.get('dry_run', False)
        queryfilter = request.POST['queryfilter'].strip()
        context['queryfilter'] = queryfilter
        users = CustomUser.objects.filter(is_active=True)
        if queryfilter:
            users = eval(queryfilter.strip())
        for user in users:
            matched_users.append(user.email)
            if TaskUser.objects.filter(user=user,
                                       task__pk=task_pk):
                skip += 1
                continue
            else:
                if selected_email:
                    email = TaskEmail.objects.get(pk=selected_email)
                if not dry_run:
                    responses = user_touch.send(None,
                                                user=user,
                                                task_slug=task.slug)
                    if email:
                        taskusers = TaskUser.objects.filter(user=user,
                                                            task__pk=task_pk)
                        for taskuser in taskusers:
                            email.taskusers.add(taskuser)
                count += 1
        context['matched_users'] = matched_users
    context['emails'] = TaskEmail.objects\
                        .filter(taskuser__task=task)\
                        .distinct()
    context['dry_run'] = dry_run
    context['count'] = count
    context['skip'] = skip
    context['selected_email'] = email
    return render_with_context(request,
                               'tasks/manage_assign_tasks.html',
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
    
