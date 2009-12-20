from django.core import mail

from signup.models import Constituency, CustomUser, RegistrationProfile
from signup.unit_tests.testbase import TestCase

from tasks.models import Project, Task, TaskUser

from tests import constituencies, users

class TestTSCAssignment(TestCase):
    """
        Makes sure the invite task is assigned to users on sign up
    """

    def setUp(self):
        """
            Create the task and add some constituencies for users
        """
        tsc = Project.objects.create(name="tsc")
        Task.objects.create(name="Upload a leaflet", slug="upload-leaflet", email="Honk", project=tsc)
        
        self.constituencies = []
        for const, yr in constituencies:
            const = Constituency.objects.create(name=const,
                                                year=yr)
            const.save()
            self.constituencies.append(const)
    
    def test_signup(self):
        """
            Test that the invite task is assigned to all users on activation
        """
        response = self.client.post("/", users[0])
        self.assertEqual(response.status_code, 302)

        user = CustomUser.objects.get()
        user.seen_invite = True
        user.save()
        user_profile = user.registrationprofile_set.get()
        
        response = self.client.get("/activate/%s/" % user_profile.activation_key)
        self.assertEqual(response.status_code, 302)

        self.assertTrue("Upload a leaflet" in mail.outbox[1].subject)
        
        response = self.client.get("/welcome", follow=True)
        
        self.assertTrue("Upload a leaflet" in response.content)

