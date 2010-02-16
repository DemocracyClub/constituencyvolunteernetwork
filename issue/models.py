from django.db import models
from django.conf import settings

from tasks.models import Task
from signup.models import Constituency, CustomUser

STATUS_CHOICES = (
    ('new', 'New'),
    ('approved', 'Approved'),
    ('hide', 'Hide'),
)

class Issue(models.Model):
    question = models.TextField()
    reference_url = models.URLField(max_length=2048, # reasonable maximum: http://www.boutell.com/newfaq/misc/urllength.html
                                    blank=True,
                                    null=True) 
    constituency = models.ForeignKey(Constituency)
    created_by = models.ForeignKey(CustomUser)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')

    last_updated_by = models.ForeignKey(CustomUser, null=True, related_name='issues_last_updater')

    def __unicode__(self):
        return self.question

    class Meta:
        get_latest_by = 'created_at'
        
