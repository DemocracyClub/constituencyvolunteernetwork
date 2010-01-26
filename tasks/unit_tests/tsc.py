from django.core import mail

from signup.models import Constituency, CustomUser, RegistrationProfile
from signup.unit_tests.testbase import TestCase

from tasks.models import Project, Task, TaskUser

from tests import users

class TestTSCAssignment(TestCase):
    """
        Makes sure the invite task is assigned to users on sign up
    """
    fixtures = ['default_data.json', 'example_data.json']

    def setUp(self):
        """
            Create the task and add some constituencies for users
        """
   
    def test_signup(self):
        """
            Test that the invite task is assigned to all users on activation
        """
        response = self.client.post("/", users[0]) # Gives "Can't find Glasgow North" error?
        self.assertRedirects(response, '/welcome', 200)

        user = CustomUser.objects.get(username="f")
        user.seen_invite = True
        user.save()
        user_profile = user.registrationprofile_set.get()
        
        response = self.client.get("/login/%s/" % user_profile.activation_key)
        self.assertEqual(response.status_code, 302)

        self.assertTrue("Upload a leaflet" in mail.outbox[1].subject)
        
        response = self.client.get("/welcome", follow=True)
        
        self.assertTrue("Upload a leaflet" in response.content)

