from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from models import Task, TaskUser
from signup.views import render_with_context

from tasks.util import login_key

def home(request):
    context = {}

    if request.user.is_authenticated():
        context['usertasks'] = TaskUser.objects.filter(user=request.user)

    return render_with_context(request, 'tasks/tasks.html', context)

@login_key
def task(request, slug):
    """
        Check out a task. Needs to also optionally take a login token to allow
        direct access to the task by email.
    """
    context = {}
   
    context['task'] = Task.objects.get(slug=slug)
    
    if request.user.is_authenticated():
        try:
            context['usertask'] = TaskUser.objects.get(task=context['task'],
                                                       user=request.user)
        except TaskUser.DoesNotExist:
            pass
    else:
        context['usertask'] = None
    
    return render_with_context(request, 'tasks/task_page.html', context)

@login_key
@login_required
def start_task(request, slug):
    """
        Mark this task as started by this user,then redirect the user to
        the task url
    """
    task = Task.objects.get(slug=slug)

    try:
        task_user = TaskUser.objects.get(task=task, user=request.user)
        task_user.state = 1
        task_user.save()
            
        return HttpResponseRedirect(task_user.url)
    except TaskUser.DoesNotExist:
        raise Http404()

@login_required
def ignore_task(request, slug):
    """
        Ignore the task then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug, user=request.user)
    task_user.ignore()
    
    return HttpResponseRedirect(reverse("task", args=[slug]))

@login_required
def unignore_task(request, slug):
    """
        Unignore the task then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug, user=request.user)
    task_user.state = 0
    task_user.save()
    
    return HttpResponseRedirect(reverse("task", args={slug: slug}))

@login_key
@login_required
def complete_task(request, slug):
    """
        Mark the task as complete then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug, user=request.user)
    task_user.complete()

    if task_user.post_url:
        return HttpResponseRedirect(task_user.post_url)
    else:
        return HttpResponseRedirect(reverse("task", args={slug: slug}))

