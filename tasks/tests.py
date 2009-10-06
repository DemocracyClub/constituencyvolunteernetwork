import datetime

from django.conf import settings
from django.core.urlresolvers import reverse

from signup.models import Constituency, CustomUser
from signup.unit_tests.testbase import TestCase

from models import Project, Task, TaskUser
import views

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
         
this_year = settings.CONSTITUENCY_YEAR
last_year = settings.CONSTITUENCY_YEAR - datetime.timedelta(365)
constituencies = [("Glasgow North", this_year),
                  ("Holborn & St Pancras", this_year),
                  ("Holborn & St Pancras", last_year)
                  ]
         
class TestInviteAssignment(TestCase):
    def setUp(self):
        dc = Project.objects.create(name="dc")
        Task.objects.create(name="Invite three friends", project=dc)
        
        self.constituencies = []
        for const, yr in constituencies:
            const = Constituency.objects.create(name=const,
                                                year=yr)
            const.save()
            self.constituencies.append(const)
    
    def test_signup(self):
        """
            Test that the invite task is assigned to all users on sign up
        """
        response = self.client.post("/", users[0])
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/")
        self.assertTrue("Invite three friends" in response.content)

class TestTaskState(TestCase):
    def setUp(self): 
        self.users = []    
        for u in users:    
            user = CustomUser.objects.create(**u)
            user.save()
            self.users.append(user)
        
        self.assertTrue(self.client.login(username="f@mailinator.com",password=""))
        
        self.dc = Project.objects.create(name="dc")
        self.task = Task.objects.create(name="Invite three friends", project=self.dc)
        self.task_user = TaskUser.objects.assign_task(self.task, self.users[0], "http://taskurl/")
        
    def test_task_assigned(self):
        response = self.client.get("/")
        self.assertTrue("start this task" in response.content)
        
    def test_task_start(self):
        response = self.client.get(reverse("start_task",  args=[self.task.slug]))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/")
        self.assertTrue("say you've completed this task" in response.content)
        self.assertTrue("ignore it" in response.content)
        
    def test_task_ignore(self):
        response = self.client.get(reverse("ignore_task", args=[self.task.slug]))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/")
        self.assertTrue("unignore this task" in response.content)
        
    def test_task_complete(self):
        response = self.client.get(reverse("complete_task",  args=[self.task.slug]))
        self.assertEqual(response.status_code, 302)
        
        response = self.client.get("/")
        self.assertTrue("completed!" in response.content)