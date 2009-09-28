from django.db import models

from slugify import smart_slugify

class Party(models.Model):
    class Meta:
        verbose_name_plural="Parties"

    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=80)

    def __unicode__(self):
        return self.name

    def get_absolute_url(self):
        return ("/parties/%s" % self.slug)

    def save(self, *args, **kwargs):
        if self.slug == "":
            self.slug = smart_slugify(self.name)
        super(Party, self).save(*args, **kwargs)

