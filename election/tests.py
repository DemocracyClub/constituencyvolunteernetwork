"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
import datetime

from django.test import TestCase

from election.models import Party, Constituency, Candidate

class TestModels(TestCase):
    def test_party_slug(self):
        # party auto-slugs on save
        p = Party(name="Monster Raving Looney")
        p.save()
        self.assertEquals("Monster-Raving-Looney", p.slug)

    def test_cand_slug(self):
        # candidate auto-slugs
        p = Party.objects.create(name="Foo")
        con = Constituency.objects.create(name="Bar", year=datetime.date(2009,1,1))
        c = Candidate.objects.create(name="Will Fibble", party=p, constituency=con)
        self.assertEquals("Will-Fibble", c.slug)
        
