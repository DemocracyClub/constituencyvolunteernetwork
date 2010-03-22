from django.db import models

from tasks.models import Task
from signup.models import Model, CustomUser

class YNMPAction(Model):
    user = models.ForeignKey(CustomUser)
    points_awarded = models.IntegerField()
    task = models.CharField(max_length=32)
    summary_of_task = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return "%s did %s (%s) getting %d points" % (self.user,
                                                     self.task,
                                                     self.summary_of_task,
                                                     self.points_awarded)

