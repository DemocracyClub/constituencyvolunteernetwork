"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase

from election.models import Party

class TestModels(TestCase):
    def test_party_slug(self):
        # party auto-slugs on save
        p = Party(name="Monster Raving Looney")
        p.save()
        self.assertEquals("Monster-Raving-Looney", p.slug)
