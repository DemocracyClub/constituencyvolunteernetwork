from django.db import models

from tasks.models import Task
from signup.models import Model, CustomUser

class MeetingInterest(Model):
    user = models.ForeignKey(CustomUser)
    date = models.DateTimeField(auto_now_add=True)
    postcode = models.CharField(max_length=9)
    organiser = models.BooleanField(default=False)
    
    def __unicode__(self):
        return "Meeting interest suggested by %s" % self.user

class MeetingInterestCompletenessTask(Task):
    class Meta:
        proxy = True
        
    def percent_complete(self):
        count = MeetingInterest.objects\
                .filter(organiser=True)\
                .count()
        return int(float(count)/600 * 100)
