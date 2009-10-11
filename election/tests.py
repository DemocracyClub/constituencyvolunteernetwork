import datetime

from django.test import TestCase

from election.models import Party, Constituency, Candidate

class TestModels(TestCase):
    def test_party_slug(self):
        # party auto-slugs on save
        p = Party(name="Monster Raving Looney")
        p.save()
        self.assertEquals("Monster-Raving-Looney", p.slug)


class TestCandidateSlug(TestCase):
    def setUp(self):
        p = Party.objects.create(name="Foo")
        con = Constituency.objects.create(
            name="Bar",
            year=datetime.date(2009,1,1))
        self.cand = Candidate.objects.create(
            name="Will Fibble",
            party=p,
            constituency=con)

    def test_cand_slug(self):
        # candidate auto-slugs
        self.assertEquals("Will-Fibble", self.cand.slug)
        
    def test_cand_slug_edit(self):
        # editing a candidate's name does not change their slug (so
        # inbound links are not broken)
        self.cand.name = "Bill Dibble"
        self.cand.save()
        self.assertEquals("Will-Fibble", self.cand.slug)
        
    def test_cand_slug_canedit(self):
        # slug can be changed (via model instance)
        self.cand.slug = "Nice-Slug"
        self.cand.save()
        self.assertEquals("Nice-Slug", self.cand.slug)
