import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.core import mail

from settings import CONSTITUENCY_YEAR as this_year

from signup.models import Constituency, CustomUser, RegistrationProfile
from signup.unit_tests.testbase import TestCase

from tasks.models import Project, Task, TaskUser, TaskEmail, TaskEmailUser
import tasks.views as views
from signup.unit_tests.test_views import create_activated_user

dc_project = {'name': 'Democracy Club',
               'slug': 'Democracy Club',
               'description': 'Stuff',
               'url': 'http://www.democracyclub.org.uk/',}

issue_task = {'name': 'Describe local issues',
              'slug': 'describe-local-issues',
              'description': ' ',
              'short_description': ' ',
              'decorator_class': 'tasks.models.ConstituencyCompletenessTask', }

issue_welcome_email = {'subject': 'Describe local issues in %(constituency)s',
                       'body': 'Dear %(name)s',
                       'count': 0,
                       'email_type': TaskEmail.EmailTypes.welcome, }

class TestTaskEmails(TestCase):
    """
        Make sure the task state changes as appropriate on the activation of
        various links
    """

    def setUp(self): 
        """
            Add a user and login as them, then create a project and some tasks
        """
        self.dc = Project.objects.create(**dc_project)
        self.task = Task.objects.create(project=self.dc, **issue_task)
        self.welcome_email = TaskEmail.objects.create(task=self.task, **issue_welcome_email)

        self.constituency = Constituency.objects.create(
            name = "Glasgow North",
            year = "2010-01-01",
            lat = "53.2797662137",
            lon = "-2.38760476605",)
        
        self.user = create_activated_user(self, "G206BT")
        self.taskuser = self.user.taskuser_set.get()
        self.welcome_email_user = self.taskuser.taskemailuser_set.get()

    def _oneoff_email(self):
        issue_oneoff_email = {'subject': 'Remember to describe local issues in %(constituency)s! oneoff',
                       'body': 'Dear %(name)s',
                       'count': 0,
                       'email_type': TaskEmail.EmailTypes.oneoff, }
        self.oneoff_email = TaskEmail.objects.create(**issue_oneoff_email)
        self.oneoff_email_user = TaskEmailUser.objects.create(task_user=self.taskuser,
                                                              task_email=self.oneoff_email,)

    def _reminder_email(self):
        issue_reminder_email = {'subject': 'Remember to describe local issues in %(constituency)s!',
                       'body': 'Dear %(name)s',
                       'count': 0,
                       'email_type': TaskEmail.EmailTypes.reminder, }
        self.reminder_email = TaskEmail.objects.create(**issue_reminder_email)
        self.reminder_email_user = TaskEmailUser.objects.create(task_user=self.taskuser,
                                                                task_email=self.reminder_email,)
        
    def test_task_assigned(self):
        """
            Make sure the task is assigned/suggested to the user on their
            front page
        """
        response = self.client.get("/welcome")
        
        self.assertTrue("Begin task" in response.content)
        self.assertTrue("Describe local issues in Glasgow North" in response.content)

    def test_welcome_email_assigned(self):
        """
            Has the user been assigned the welcome email?
        """
        
        self.assertEqual(self.welcome_email_user.task_user, self.taskuser)
        self.assertEqual(self.welcome_email_user.task_email, self.welcome_email)
        self.assertEqual(self.welcome_email_user.date_sent, None)

    def test_queue(self):
        # Ping the queue
        queue_response = self.client.get("/tasks/admin/queue")
        
        self.welcome_email_user = self.taskuser.taskemailuser_set.get()

        self.assertTrue(self.welcome_email_user.date_sent is not None)
        self.assertTrue("a@b.com, Describe local issues, Describe local issues in %(constituency)s" in queue_response.content)
        self.assertTrue("Describe local issues in %s" % self.constituency.name in mail.outbox[1].subject)
        
        # Send the oneoff email (won't work, too soon after reminder)
        self._oneoff_email()
        queue_response = self.client.get("/tasks/admin/queue")
        self.assertTrue(len(mail.outbox) == 2)

        # Artificially set the welcome email to have happened 2 days ago and try again
        self.welcome_email_user.date_sent -= datetime.timedelta(2)
        self.welcome_email_user.save()
        queue_response = self.client.get("/tasks/admin/queue")
        self.assertTrue(len(mail.outbox) == 3)
        self.assertTrue("Remember to describe local issues in %s! oneoff" % self.constituency.name in mail.outbox[2].subject)
        
        self.oneoff_email_user = TaskEmailUser.objects.get(task_user=self.taskuser,
                                                           task_email=self.oneoff_email)

        # Send the reminder email (won't work, too soon after oneoff)
        self._reminder_email()
        queue_response = self.client.get("/tasks/admin/queue")
        self.assertTrue(len(mail.outbox) == 3)

        self.reminder_email_user = TaskEmailUser.objects.get(task_user=self.taskuser,
                                                             task_email=self.reminder_email)

        # Artificially set the oneoff email to have happened 2 days ago and try again
        self.oneoff_email_user.date_sent -= datetime.timedelta(2)
        self.oneoff_email_user.save()
        queue_response = self.client.get("/tasks/admin/queue")
        self.assertTrue(len(mail.outbox) == 4)
        self.assertTrue("Remember to describe local issues in %s!" % self.constituency.name in mail.outbox[3].subject)
        
        self.reminder_email_user = TaskEmailUser.objects.get(task_user=self.taskuser,
                                                             task_email=self.reminder_email)

        # Try sending the reminder email again (won't work, was last sent less than 7 days ago)
        queue_response = self.client.get("/tasks/admin/queue")
        self.assertTrue(len(mail.outbox) == 4)

        # Artificially set the reminder email to have happened 7 days ago and try again
        self.reminder_email_user.date_sent -= datetime.timedelta(7)
        self.reminder_email_user.save()
        queue_response = self.client.get("/tasks/admin/queue")
        self.assertTrue(len(mail.outbox) == 5)
        self.assertTrue("Remember to describe local issues in %s!" % self.constituency.name in mail.outbox[4].subject)
        
        self.reminder_email_user = TaskEmailUser.objects.get(task_user=self.taskuser,
                                                             task_email=self.reminder_email)

        # Set competition between the oneoff email and the reminder email
        self._oneoff_email()
        self.reminder_email_user.date_sent -= datetime.timedelta(7)
        self.reminder_email_user.save()
        queue_response = self.client.get("/tasks/admin/queue")
        self.assertTrue(len(mail.outbox) == 6) # Only one sends
        self.assertTrue("Remember to describe local issues in %s! oneoff" % self.constituency.name in mail.outbox[5].subject)

