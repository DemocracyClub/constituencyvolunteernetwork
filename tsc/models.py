from django.db import models
from signup.models import Model, CustomUser

class UploadedLeaflet(Model):
    url = models.URLField()
    user = models.ForeignKey(CustomUser)
    date = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return "Leaflet uploaded by %s to %s on %s" % (self.user, self.url, self.date)

