from django.db import models
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

class TaskUser(Model):
    task = models.ForeignKey(Task)
    user = models.ForeignKey(CustomUser)
    state = models.SmallIntegerField(choices=TASK_STATES)
    date_assigned = models.DateTimeField(auto_now_add=True)
    url = models.URLField()
    
    objects = TaskUserManager()
    
    def state_string(self):
        return task_state_string[self.state]
    
    def __unicode__(self):
        return "%s doing %s (%s)" % (self.user, self.task, task_state_string[self.state])