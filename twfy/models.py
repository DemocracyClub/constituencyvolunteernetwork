from django.db import models

from signup.models import Model
from issue.models import RefinedIssue

from ynmp.models import Candidacy

class Statement(Model):
    twfy_key = models.CharField(max_length=20)
    refined_issue = models.ForeignKey(RefinedIssue,
                                      blank=True,
                                      null=True)
    question = models.CharField(max_length=350,
                                blank=True,
                                null=True)
    national = models.BooleanField(default=False)

class SurveyResponse(Model):
    candidacy = models.ForeignKey(Candidacy)
    statement = models.ForeignKey(Statement)
    national = models.BooleanField(default=False)
    # 100 = strongly agree, 0 = strongly disagree
    agreement = models.IntegerField()
    more_explanation = models.TextField()
                                        
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
