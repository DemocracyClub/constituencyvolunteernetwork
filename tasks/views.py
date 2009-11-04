from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse, Http404
from django.core.urlresolvers import reverse

from signup.views import render_with_context
from models import Task, TaskUser


def home(request):
    context = {}

    if request.user.is_authenticated():
        context['usertasks'] = TaskUser.objects.filter(user=request.user)

    return render_with_context(request, 'tasks/tasks.html', context)

def task(request, slug, login_token=None):
    """
        Check out a task. Needs to also optionally take a login token to allow
        direct access to the task by email.
    """
    context = {}
    
    context['task'] = Task.objects.get(slug=slug)
    
    try:
        context['usertask'] = TaskUser.objects.get(task=context['task'],
                                                   user=request.user)
    except Taskuser.DoesNotExist:
        pass
    
    return render_with_context(request, 'tasks/task_page.html', context)


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


def ignore_task(request, slug):
    """
        Ignore the task then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug, user=request.user)
    task_user.ignore()
    
    return HttpResponseRedirect(reverse("task", args={slug: slug}))


def unignore_task(request, slug):
    """
        Unignore the task then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug, user=request.user)
    task_user.state = 0
    task_user.save()
    
    return HttpResponseRedirect(reverse("task", args={slug: slug}))


def complete_task(request, slug):
    """
        Mark the task as complete then redirect the user to the front page
    """
    task_user = TaskUser.objects.get(task__slug=slug, user=request.user)
    task_user.complete()
    
    return HttpResponseRedirect(reverse("task", args={slug: slug}))
