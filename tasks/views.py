from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required
from django.utils.http import urlquote
from django.db.models import Count

from models import Task, TaskUser
from models import Badge
from signup.models import CustomUser, Constituency
from signup.views import render_with_context
from signup.views import _get_statistics_context

from tasks.util import login_key

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
    if constituencies:
        # the strange way we construct the query with "__id__in"
        # operators is necessary because otherwise we get
        # subquery-related complaints from postgres
        ids = [x.id for x in constituencies]
        context['activity'] = TaskUser.objects\
          .filter(user__constituencies__id__in=ids)\
          .filter(state__in=[TaskUser.States.started,
                            TaskUser.States.completed])\
          .order_by('-date_modified').distinct().all()
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
        context['constituency'] = Constituency.objects.get(slug=constituency)
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
        context['usertask'] = None

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
        
        task_user.state = TaskUser.States.started
        task_user.save()
        url = task_user.url
        if task_user.post_url:
            url += "?callback=" + urlquote(task_user.post_url)
        return HttpResponseRedirect(url)
    except TaskUser.DoesNotExist:
        raise Http404()

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
            all_users = CustomUser.objects.all()
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
            all_users = CustomUser.objects.filter(constituencies__in=constituencies)
            
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

