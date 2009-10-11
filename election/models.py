from django.db import models
from django.db.models.signals import pre_save

from signup.models import Constituency

from slugify import smart_slugify

def slug_on_save(sender, instance, **kwargs):
    "signal handler - adds slug if it is not set"
    if instance.slug == "":
        instance.slug = smart_slugify(instance.name)


class Party(models.Model):
    """
    A Political party.
    """
    class Meta:
        verbose_name_plural="Parties"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        return self.name

pre_save.connect(slug_on_save, sender=Party)


class Candidate(models.Model):
    """
    A Candidate stands in a constituency, possibly reprisenting a party.
    """
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    party = models.ForeignKey(Party)
    constituency = models.ForeignKey(Constituency)
    email = models.EmailField(blank=True)

    def __unicode__(self):
        return self.name

pre_save.connect(slug_on_save, sender=Candidate)
