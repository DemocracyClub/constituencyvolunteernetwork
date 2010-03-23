import re

from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.db.models import Count

from tasks.models import Task, TaskUser, Badge
from signup.signals import *
from signals import *

import settings
from tasks.util import reverse_login_key
from tasks.decorators import task_assign, task_completion
from signup.models import Constituency

task_slug = "describe-local-issues"

@task_completion(task_slug)
def callback_issue_added(sender, **kwargs):
    """
        Set this task as complete if they've added one issue.
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']
    issue = kwargs['issue']

    # Only do the task once?
    if task_user.state != TaskUser.States.completed:
        task_user.complete()

    try:
        badge = Badge.objects.get(task=task, user=user)
        match = re.search(r"Added (.+) local issue",
                          badge.name).group(1)
        if match == 'a':
            name = "Added 2 local issues"
        else:
            name = "Added %d local issues" % (int(match) + 1)
        badge.name = name
        badge.save()
    except Badge.DoesNotExist:
        badge = Badge.objects.create(name="Added a local issue",
                                     task=task,
                                     user=user)


@task_assign(task_slug)
def callback_assign(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and isn't
        already doing the task.
    """
    user = kwargs['user']
    task = kwargs['task']

    constituencies = None
    if "constituencies" in kwargs and kwargs['constituencies'] is not None:
        constituencies = kwargs['constituencies']
    else:
        constituencies = user.current_constituencies

    current_site = Site.objects.get_current()
    assigned = []
    for constituency in constituencies:
        kwargs = {'constituency': constituency.slug}
        add_issue_url = reverse("add_issue", kwargs=kwargs)
        try:                
            TaskUser.objects.assign_task(task,
                                         user,
                                         add_issue_url,
                                         constituency=constituency)
        except TaskUser.AlreadyAssigned:
            msg = "%s already assigned to %s in %s"
            assigned.append(msg % (task, user, constituency))
    return "; ".join(assigned)

# Assignment signals
user_activated.connect(callback_assign)
user_touch.connect(callback_assign)
user_join_constituency.connect(callback_assign)

# Completion signals
issue_added.connect(callback_issue_added)

###################
task_slug = "describe-local-issues-2"

@task_completion(task_slug)
def callback_issue_added_2(sender, **kwargs):
    """
        Set this task as complete if they've added one issue.
    """
    user = kwargs['user']
    task = kwargs['task']
    task_user = kwargs['task_user']
    issue = kwargs['issue']

    # Only do the task once?
    if task_user.state != TaskUser.States.completed:
        task_user.complete()

    try:
        badge = Badge.objects.get(task=task, user=user)
        match = re.search(r"Added (.+) local issue",
                          badge.name).group(1)
        if match == 'a':
            name = "Added 2 local issues"
        else:
            name = "Added %d local issues" % (int(match) + 1)
        badge.name = name
        badge.save()
    except Badge.DoesNotExist:
        badge = Badge.objects.create(name="Added a local issue",
                                     task=task,
                                     user=user)


@task_assign(task_slug)
def callback_assign_2(sender, **kwargs):
    """
        Assign this task to everyone who activates the signals and isn't
        already doing the task.
    """
    user = kwargs['user']
    task = kwargs['task']

    constituencies = None
    if "constituencies" in kwargs and kwargs['constituencies'] is not None:
        constituencies = kwargs['constituencies']
    else:
        constituencies = user.current_constituencies

    current_site = Site.objects.get_current()
    assigned = []
    for constituency in constituencies:
        kwargs = {'constituency': constituency.slug}
        add_issue_url = reverse("add_issue", kwargs=kwargs)
        try:                
            TaskUser.objects.assign_task(task,
                                         user,
                                         add_issue_url,
                                         constituency=constituency)
        except TaskUser.AlreadyAssigned:
            msg = "%s already assigned to %s in %s"
            assigned.append(msg % (task, user, constituency))
    return "; ".join(assigned)

# Assignment signals
user_activated.connect(callback_assign_2)
user_touch.connect(callback_assign_2)
user_join_constituency.connect(callback_assign_2)

# Completion signals
issue_added.connect(callback_issue_added_2)

