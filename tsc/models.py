from django.db import models

from signup.models import Model, CustomUser, Constituency
from tasks.models import Task
from tasks.models import TaskUser

class UploadedLeaflet(Model):
    url = models.URLField()
    user = models.ForeignKey(CustomUser)
    date = models.DateTimeField(auto_now_add=True)
    constituency = models.ForeignKey(Constituency)

    def __unicode__(self):
        return "Leaflet uploaded by %s to %s on %s" % (self.user,
                                                       self.url,
                                                       self.date) 
