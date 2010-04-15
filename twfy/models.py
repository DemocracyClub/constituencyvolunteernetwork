from django.db import models

from signup.models import Model
from ynmp.models import Candidacy

class SurveyInvite(Model):
    ynmp_id = models.CharField(max_length=9)
    candidacy = models.ForeignKey(Candidacy,
                                  blank=True,
                                  null=True)
    emailed = models.BooleanField(default=False)
    filled_in = models.BooleanField(default=False)
