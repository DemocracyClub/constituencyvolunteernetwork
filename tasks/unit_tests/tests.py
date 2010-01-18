import datetime

from django.conf import settings
from django.core.urlresolvers import reverse

from signup.models import Constituency, CustomUser, RegistrationProfile
from signup.unit_tests.testbase import TestCase

from tasks.models import Project, Task, TaskUser
import tasks.views

users = [{'email':'f@mailinator.com',
          'postcode':'G206BT',
          'can_cc':True,
          'first_name':'f',
          'last_name':'f',
          'username':'f@mailinator.com'},
         {'email':'g@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':True,
          'first_name':'g',
          'last_name':'g',
          'username':'g@mailinator.com'},
         {'email':'h@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':False,
          'first_name':'hoogly',
          'last_name':'h',
          'username':'h@mailinator.com'},
         ]


class TestTaskState(TestCase):
    """
        Make sure the task state changes as appropriate on the activation of
        various links
    """

    def setUp(self): 
        """
            Add a user and login as them, then create a project and some tasks
        """
        self.users = []    
        for u in users:    
            user = CustomUser.objects.create(**u)
            user.save()
            profile = RegistrationProfile.objects.create_profile(user)
            self.users.append(user)
        
        self.assertTrue(self.client\
            .login(username="f@mailinator.com", password=""))
        self.dc = Project.objects.create(name="dc")
        self.task = Task.objects\
            .create(name="Invite three friends", project=self.dc)
        self.task_user = TaskUser.objects\
            .assign_task(self.task, self.users[0], "http://taskurl/")
        
    def test_task_assigned(self):
        """
            Make sure the task is assigned/suggested to the user on their
            front page
        """
        response = self.client.get("/")
        self.assertTrue("start this task" in response.content)
        
    def test_task_start(self):
        """
            Start the task and make sure the state of the task
            on the front page has changed appropriately
        """
        response = self.client.get(reverse("start_task",\
                                   args=[self.task.slug]))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/")
        self.assertTrue("say you've completed this task" in response.content)
        self.assertTrue("ignore it" in response.content)
        
    def test_task_ignore(self):
        """
            Ignore the task and make sure the state of the task
            on the front page has changed appropriately
        """
        response = self.client.get(reverse("ignore_task",
                                   args=[self.task.slug]))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/")
        self.assertTrue("unignore this task" in response.content)
        
    def test_task_complete(self):
        """
            Mark the task complete and make sure the state of the
            task on the front page has changed appropriately
        """
        response = self.client.get(reverse("complete_task",
                                   args=[self.task.slug]))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/")
        self.assertTrue("completed!" in response.content)
