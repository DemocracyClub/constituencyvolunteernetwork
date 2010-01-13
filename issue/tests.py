"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

    def test_enter_issue(self):
        response = self.client.post("/issue", { 'title' : "Reopen children's A&E in Southport",
            'reference_url' : 'http://www.liverpoolecho.co.uk/liverpool-news/local-news/2009/07/20/taxis-in-go-slow-support-for-southport-a-e-100252-24193098/' })
        # http://www.cares.ukhome.net/
        self.assertEqual

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

