from django.db import models
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings

from signup.models import Model, CustomUser

class Project(Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    description = models.TextField()
    url = models.URLField()
    
    def __unicode__(self):
        return self.name
    
class Task(Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    project = models.ForeignKey(Project)
    description = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(CustomUser, through="TaskUser")
    
    def __unicode__(self):
        return self.name
    
TASK_STATES = (
    (0, 'Assigned'),
    (1, 'Started'),
    (2, 'Ignored'),
    (3, 'Completed'),
)

task_state_string = {0: 'Assigned', 1:'Started', 2:'Ignored', 3:'Completed'}

class TaskUserManager(models.Manager):
    def assign_task(self, task, user, url):
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
    task = models.ForeignKey(Task)
    user = models.ForeignKey(CustomUser)
    state = models.SmallIntegerField(choices=TASK_STATES)
    date_assigned = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    
    objects = TaskUserManager()
    
    def state_string(self):
        return task_state_string[self.state]
        
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
        return "%s doing %s (%s)" % (self.user, self.task, task_state_string[self.state])