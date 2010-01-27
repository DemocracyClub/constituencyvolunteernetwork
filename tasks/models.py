from django.db import models
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.conf import settings
from django.core.urlresolvers import reverse

from signup.models import Model, CustomUser
from signup.models import Constituency
from signup.signals import user_leave_constituency

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
    url = models.URLField(verify_exists = False) # verify_exists is a pain when coding offline

    def __unicode__(self):
        return self.name


class Task(Model):
    """
        A description of a task, attached to a project (optionally), with a
        list of users doing the task
    """
    name = models.CharField(max_length=80)
    email_subject = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    project = models.ForeignKey(Project)
    description = models.TextField()
    email = models.TextField(verbose_name="Description for email")
    date_created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(CustomUser, through="TaskUser")
    decorator_class = models.CharField(max_length=180)
    
    def __unicode__(self):
        return self.name

    def get_started_users(self):
        return CustomUser.objects.filter(taskuser__task=self, taskuser__state=1)

    @models.permalink
    def get_absolute_url(self):
        return ("task", (self.slug,))

    def percent_complete(self):
        """Return a measure of completeness for this task.

        The default behavious is the proportion of users who have
        completed the task.  However, individual Tasks may implement
        their own version of this calculation via a Django Proxy model
        registered as a 'decorator_class' method (see __getattr__
        below).        
        """
        try:
            return self.__getattr__('percent_complete')()
        except AttributeError:
            return self._percent_complete_default()

    def _percent_complete_default(self):
        all_users = CustomUser.objects\
                    .filter(is_active=True,
                            taskuser__task=self,
                            taskuser__state__in=[TaskUser.States.started,
                                                 TaskUser.States.completed,
                                                 TaskUser.States.assigned])
        completed = all_users.filter(taskuser__task=self,
                                     taskuser__state=TaskUser.States.completed)
        if all_users.count():
            percent = int(float(completed.count())/all_users.count() \
                          * 100)
        else:
            percent = 0
        return percent

    def __getattr__(self, attr):
        """Individual applications may extend the Python behaviour of
        the Task model.

        This is achieved using a Django Proxy model, the dotted
        reference to which is stored in the (optional)
        'decorator_class' field.
        
        """
        target = None
        if self.decorator_class:
            parts = self.decorator_class.split(".")                    
            _temp = __import__(".".join(parts[:-1]),
                               None,
                               None,
                               [parts[-1]]) 
            klass = getattr(_temp, parts[-1])
            decorated_obj = klass.objects.get(pk=self.pk)
            if hasattr(klass, attr):
                # this test prevents recursion
                target = getattr(decorated_obj, attr)
        if not target:
            error = "%s instance has no attribute '%s'"
            error = error % (self.__class__.__name__, attr)
            raise AttributeError, error
        else:
            return target

class ConstituencyCompletenessTask(Task):
    class Meta:
        proxy = True
        
    def percent_complete(self):
        year = settings.CONSTITUENCY_YEAR
        total = Constituency.objects.filter(year=year).count()
        count = Constituency.objects.filter(issue__isnull=False).count()
        return int(float(count)/total * 100)


class TaskUserManager(models.Manager):
    """
        Managing the TaskUser objects
    """
    def trigger_assign(self, task, user_set, constituencies=None):
        from signup.signals import user_touch
        
        assigned = []
        already_assigned = []
        for user in user_set:
            user_touch.send(self, user=user, task_slug=task.slug, constituencies=constituencies)
            assigned.append(user)

        return (assigned, already_assigned)
        
    def assign_task(self, task, user, url,
                    post_url=None,
                    constituency=None,
                    email=False):
        if TaskUser.objects.filter(task=task,
                                   user=user,
                                   constituency=constituency):
            raise TaskUser.AlreadyAssigned()
        
        task_user = TaskUser(task=task,
                             user=user,
                             state=0,
                             url=url,
                             post_url=post_url,
                             constituency=constituency)
        task_user.save()
        if email:
            task_user.send_email()
        
        signals.task_assigned.send(self, task_user=task_user)

class TaskUser(Model):
    """
        Describes the mapping between Tasks and Users,
        i.e. what tasks a user can do, and their state for those tasks.
        
        These objects are created by tasks on reception of signals, allowing
        them to apply their own criteria for assignment (e.g. users in
        a particular constituency)
    """
    class States:
        """ Enum of TaskUser states """
        assigned = 0
        started = 1
        completed = 2
        ignored = 3

        strings = (
            (assigned, 'assigned'),
            (started, 'started'),
            (completed, 'completed'),
            (ignored, 'ignored'),
        )
    
    task = models.ForeignKey(Task)
    user = models.ForeignKey(CustomUser)
    constituency = models.ForeignKey(Constituency, null=True, blank=True)
    state = models.SmallIntegerField(choices=States.strings)
    date_assigned = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True, auto_now_add=True)
    url = models.CharField(max_length=2048)
    post_url = models.CharField(max_length=2048, null=True, blank=True)
    emails_sent = models.IntegerField(default=0)
    objects = TaskUserManager()
    
    task_state_string = dict(States.strings)

    # internal helper, returns dictionary of URL construction arguments
    def _get_kwargs(self):
        kwargs = {'slug': self.task.slug}
        if self.constituency:
            kwargs['constituency'] = self.constituency.slug
        return kwargs

    def description_link(self):
        href = '<a class="usertask" href="%s">%s</a>'
        name = self.task.name
        if self.constituency:
            name += " in %s" % self.constituency.name
        return href % (reverse("task", kwargs=self._get_kwargs()), name)

    def get_absolute_url(self):
        return reverse("task", kwargs=self._get_kwargs())

    def transition_links(self):
        links = []
        href = '<a href="%s" class="action %s">%s</a>'
        if self.state == self.States.assigned:
            url = reverse("start_task", kwargs=self._get_kwargs())
            links.append(href % (url,
                                "start-task",
                                 "Begin task"))
        elif self.state == self.States.started:
            url = reverse("start_task", kwargs=self._get_kwargs())
            links.append(href % (url,
                                "start-task",
                                 "Resume"))
            url = reverse("complete_task", kwargs=self._get_kwargs())
            links.append(href % (url,
                                 "complete-task",
                                 "Done"))
        elif self.state == self.States.ignored:
            url = reverse("unignore_task", kwargs=self._get_kwargs())
            links.append(href % (url,
                                 "unignore-task",
                                 "unignore"))
        elif self.state == self.States.completed:
            links.append('<span class="completed">' \
                         + 'You have completed this task!</span>') 
            url = reverse("start_task", kwargs=self._get_kwargs())
            links.append(href % (url,
                                "start-task",
                                 "Start it again"))

        if self.state in [self.States.assigned, self.States.started]:
            url = reverse("ignore_task",
                          kwargs=self._get_kwargs())
            links.append(href % (url,
                                 "ignore-task",
                                 "Ignore"))
        
        # a maximim of three links can appear.  Pad the list
        # so it's always 3 items long
        links.extend([''] * (3 - len(links)))
        return links
    
    def state_string(self):
        return self.task_state_string[self.state]
    
    def start(self):
        self.state = TaskUser.States.started
        self.save()

        signals.task_started.send(self, task_user=self)
    
    def complete(self):
        self.state = TaskUser.States.completed
        self.save()

        signals.task_completed.send(self, task_user=self)
    
    def ignore(self):
        self.state = TaskUser.States.ignored
        self.save()
        
        signals.task_ignored.send(self, task_user=self)

    def email(self):
        """
            Build the email text with optional url insertion points
        """
        current_site = Site.objects.get_current()
        
    def send_email(self):
        """Send an email to the user telling them about this task.
        """
        user = self.user
        task = self.task
        user_profile = user.registrationprofile_set.get()
        current_site = Site.objects.get_current()

        task_url = "http://%s%s" % (current_site.domain,
                                    reverse_login_key('start_task',
                                                      user,
                                                      kwargs=self._get_kwargs()))
        ignore_url = "http://%s%s" % (current_site.domain,
                                      reverse_login_key('ignore_task',
                                                        user,
                                                        kwargs=self._get_kwargs()))
        post_url = "http://%s%s" % (current_site.domain,
                                    reverse_login_key('complete_task',
                                                      user,
                                                      kwargs=self._get_kwargs()))

        description_text = task.email % \
            {'task_url': task_url,
            'post_url': post_url,}

        email_context = {'task': task,
                         'user': user,
                         'task_user': self,
                         'task_url': task_url,
                         'ignore_url': ignore_url,
                         'post_url': post_url,
                         'description_text': description_text,
                         'site': current_site,
                         'user_profile': user_profile,}

        message = render_to_string('tasks/email_new_task.txt',
                                   email_context)
        message_html = render_to_string('tasks/email_new_task.html',
                                   email_context)

        # Now using EmailMultiAlternatives to send HTML version
        msg = EmailMultiAlternatives(task.email_subject,
                                     message,
                                     settings.DEFAULT_FROM_EMAIL,
                                     [user.email, ])
        msg.attach_alternative(message_html, "text/html")
        msg.send()
        self.emails_sent += 1
        self.save()
    
    def __unicode__(self):
        return "%s doing %s (%s)" % (self.user, self.task, self.state_string())
    
    class AlreadyAssigned(Exception):
        """
            Thrown by the UserTaskManager on attempted
            assignment/suggestion of a task which a user already has
        """
        pass

def callback_user_left_constituency(sender, **kwargs):
    constituencies = kwargs['constituencies']
    user = kwargs['user']

    TaskUser.objects.filter(user=user, constituency__in=constituencies).delete()

user_leave_constituency.connect(callback_user_left_constituency)

class Badge(Model):
    name = models.CharField(max_length=80)
    task = models.ForeignKey(Task)
    user = models.ForeignKey(CustomUser)
    date_awarded = models.DateTimeField(auto_now_add=True)
    number = models.IntegerField(default=1)

    def __unicode__(self):
        return 'Badge "%s" for %s' % (self.name, self.user)
