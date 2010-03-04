import re
import urllib

from django.db import models

from signup.models import Model, CustomUser, Constituency
from tasks.models import Task
import settings

url_regex = re.compile(r'http://(www|staging).thestraightchoice.org/leaflet.php\?q=([0-9]+)')

class UploadedLeaflet(Model):
    url = models.URLField()
    user = models.ForeignKey(CustomUser)
    date = models.DateTimeField(auto_now_add=True)
    constituency = models.ForeignKey(Constituency)
    thumb_url = models.URLField(null=True, blank=True)
    
    @property
    def tsc_id(self):
        result = url_regex.findall(self.url)
        if result:
            return int(result[0][1])
        else:
            return None

    @property
    def thumbnail_url(self):
        if not self.thumb_url:
            api_call = "http://www.thestraightchoice.org/api/call.php?method=image&output=url&leaflet_id=%d&size=t" % (self.tsc_id)
            
            print api_call

            response = urllib.urlopen(api_call)

            if response:
                self.thumb_url = response.read()
                self.save()

        return self.thumb_url

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
