from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

from signup.models import Model, CustomUser

class Project(Model):
    """
        Represents a grouping of tasks belonging to a particular project/group,
        along with a description and a url for the main project website
        
        e.g. TheyWorkForYou, TheStraightChoice, DemocracyClub
    """
    
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    description = models.TextField()
    url = models.URLField()
    
    def __unicode__(self):
        return self.name
    
class Task(Model):
    """
        A description of a task, attached to a project (optionally), with a
        list of users doing the task
    """
    
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    project = models.ForeignKey(Project)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(CustomUser, through="TaskUser")
    
    def __unicode__(self):
        return self.name
        
    def get_started_users(self):
        return TaskUser.objects.filter(task=self, state=1)
    
TASK_STATES = (
    (0, 'Assigned'),
    (1, 'Started'),
    (2, 'Ignored'),
    (3, 'Completed'),
)

class TaskUserManager(models.Manager):
    """
        Managing the TaskUser objects
    """
    
    def assign_task(self, task, user, url):
        if TaskUser.objects.filter(task=task, user=user):
            raise TaskUser.AlreadyAssigned()
        
        task_user = TaskUser(task=task, user=user, state=0, url=url)
        task_user.save()
        
        current_site = Site.objects.get_current()
        subject = "New task - %s" % task.name
        email_context = {'task': task,
                         'user': user,
                         'task_user': task_user,
                         'site': current_site}
        
        message = render_to_string('tasks/email_new_task.txt',
                                   email_context)
        
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [user.email,])

class TaskUser(Model):
    """
        Describes the mapping between Tasks and Users,
        i.e. what tasks a user can do, and their state for those tasks.
        
        These objects are created by tasks on reception of signals, allowing
        them to apply their own criteria for assignment (e.g. users in
        a particular constituency)
    """
    
    task = models.ForeignKey(Task)
    user = models.ForeignKey(CustomUser)
    state = models.SmallIntegerField(choices=TASK_STATES)
    date_assigned = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    
    objects = TaskUserManager()
    
    task_state_string = dict(TASK_STATES)
    
    def state_string(self):
        return self.task_state_string[self.state]
    
    def start(self):
        self.state = 1
        self.save()
        
    def complete(self):
        self.state = 3
        self.save()
        
    def ignore(self):
        self.state = 2
        self.save()
    
    def __unicode__(self):
        return "%s doing %s (%s)" % (self.user, self.task, self.state_string())

    class AlreadyAssigned(Exception):
        """
            Thrown by the UserTaskManager on attempted assignment/suggestion of a task
            which a user already has
        """
        pass