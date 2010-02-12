from django.db import models
from django.conf import settings

from tasks.models import Task
from signup.models import Constituency, CustomUser

STATUS_CHOICES = (
    ('new', 'New'),
    ('approved', 'Approved'),
    ('junk', 'Junk'),
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

    def __unicode__(self):
        return self.question

