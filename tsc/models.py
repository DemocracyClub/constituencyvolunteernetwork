from django.db import models

from signup.models import Model, CustomUser, Constituency
from tasks.models import Task
import settings

class UploadedLeaflet(Model):
    url = models.URLField()
    user = models.ForeignKey(CustomUser)
    date = models.DateTimeField(auto_now_add=True)
    constituency = models.ForeignKey(Constituency)

    def __unicode__(self):
        return "Leaflet uploaded by %s to %s on %s" % (self.user,
                                                       self.url,
                                                       self.date) 

class ConstituencyCompletenessTask(Task):
    class Meta:
        proxy = True
        
    def percent_complete(self):
        year = settings.CONSTITUENCY_YEAR
        total = Constituency.objects\
                .filter(year=year)\
                .count()
        count = Constituency.objects\
                .filter(year=year)\
                .filter(uploadedleaflet__isnull=False)\
                .distinct()\
                .count()
        return int(float(count)/total * 100)
