from django.db import models

from signup.models import Constituency

from slugify import smart_slugify

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

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = smart_slugify(self.name)
        super(Party, self).save(*args, **kwargs)


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
    
    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = smart_slugify(self.name)
        super(Candidate, self).save(*args, **kwargs)
