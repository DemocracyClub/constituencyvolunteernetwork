from django.db import models
from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse

from signup.models import Model, CustomUser, RegistrationProfile

from tasks.util import reverse_login_key
import signals

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
    email = models.TextField()
    date_created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(CustomUser, through="TaskUser")

    def __unicode__(self):
        return self.name

    def get_started_users(self):
        return CustomUser.objects.filter(taskuser__task=self, taskuser__state=1)

    @models.permalink
    def get_absolute_url(self):
        return ("task", (self.slug,))


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
    def trigger_assign(self, task, user_set):
        from signup.signals import user_touch
        
        assigned = []
        already_assigned = []
        for user in user_set:
            try:
                user_touch.send(self, user=user, task_slug=task.slug)
                assigned.append(user)
            except TaskUser.AlreadyAssigned:
                already_assigned.append(user)

        return (assigned, already_assigned)
        
    def assign_task(self, task, user, url, post_url=None):
        if TaskUser.objects.filter(task=task, user=user):
            raise TaskUser.AlreadyAssigned()
        
        task_user = TaskUser(task=task, user=user, state=0, url=url, post_url=post_url)
        task_user.save()
        
        user_profile = user.registrationprofile_set.get()
        current_site = Site.objects.get_current()
        subject = "%s - from Democracy Club" % task.name

        task_url = "http://%s%s" % (current_site.domain, reverse_login_key('start_task', user, kwargs={'slug': task.slug}))
        post_url = "http://%s%s" % (current_site.domain, reverse_login_key('complete_task', user, kwargs={'slug': task.slug}))

        description_text = task.email % \
            {'task_url': task_url,
            'post_url': post_url,}

        email_context = {'task': task,
                         'user': user,
                         'task_user': task_user,
                         'task_url': task_url,
                         'post_url': post_url,
                         'description_text': description_text,
                         'site': current_site,
                         'user_profile': user_profile,}
        
        message = render_to_string('tasks/email_new_task.txt',
                                   email_context)
        message_html = render_to_string('tasks/email_new_task.html',
                                   email_context)

        # Now using EmailMultiAlternatives to send HTML version
        msg = EmailMultiAlternatives(subject,
                                     message,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [user.email, ])
        msg.attach_alternative(message_html, "text/html")
        msg.send()
        
        signals.task_assigned.send(self, task_user=task_user)

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
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    url = models.CharField(max_length=2048)
    post_url = models.CharField(max_length=2048, null=True, blank=True)
    
    objects = TaskUserManager()
    
    task_state_string = dict(TASK_STATES)
    
    def state_string(self):
        return self.task_state_string[self.state]
    
    def start(self):
        self.state = 1
        self.save()

        signals.task_started.send(self, task_user=self)
    
    def complete(self):
        self.state = 3
        self.save()

        signals.task_completed.send(self, task_user=self)
    
    def ignore(self):
        self.state = 2
        self.save()
        
        signals.task_ignored.send(self, task_user=self)

    def email(self):
        """
            Build the email text with optional url insertion points
        """
        current_site = Site.objects.get_current()
        
    
    def __unicode__(self):
        return "%s doing %s (%s)" % (self.user, self.task, self.state_string())
    
    class AlreadyAssigned(Exception):
        """
            Thrown by the UserTaskManager on attempted
            assignment/suggestion of a task which a user already has
        """
        pass

class Badge(Model):
    name = models.CharField(max_length=80)
    task = models.ForeignKey(Task)
    user = models.ForeignKey(CustomUser)

    def __unicode__(self):
        return 'Badge "%s" for %s' % (self.name, self.user)