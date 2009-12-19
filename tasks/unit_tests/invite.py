from signup.models import Constituency, CustomUser
from signup.unit_tests.testbase import TestCase

from tasks.models import Project, Task, TaskUser

from tests import constituencies

class TestInviteAssignment(TestCase):
    """
        Makes sure the invite task is assigned to users on sign up
    """

    def setUp(self):
        """
            Create the task and add some constituencies for users
        """
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