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
    survey_token = models.CharField(max_length=30,
                                    blank=True,
                                    null=True)
    pester_emails_sent = models.IntegerField(default=0)

    def __unicode__(self):
        number_emails = self.pester_emails_sent
        if self.emailed:
            number_emails += 1
        return "%s\t%s\t%s\t%d\t%s" % \
               (self.candidacy.candidate.name,
                self.candidacy.candidate.email,
                unicode(self.candidacy.candidate.party.name),
                number_emails,
                self.filled_in)
