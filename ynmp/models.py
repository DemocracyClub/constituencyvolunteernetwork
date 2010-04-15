from django.db import models

from tasks.models import Task
from signup.models import Model, CustomUser, Constituency

def expand_item(word):
    words = {'email': 'an email address',
             'phone': 'a phone number',
             'fax': 'a fax number',
             'address': 'a postal address',}
    return words[word]

class Party(Model):
    ynmp_id = models.CharField(max_length=9)
    name = models.CharField(max_length=255)

    def calculate_stats(self):
        self.invites_sent = SurveyInvite.objects\
                            .filter(emailed=True,
                                    candidacy__party=self)\
                                    .count()
        self.replies_received = SurveyInvite.objects\
                            .filter(filled_in=True,
                                    candidacy__party=self)\
                                    .count()
        self.save()
        
    def __unicode__(self):
        return "%s (ynmp id %s)" % (self.name,
                                    self.ynmp_id)
    
class YNMPConstituency(Model):
    constituency = models.ForeignKey(Constituency)
    ynmp_seat_id = models.CharField(max_length=9)

    def __unicode__(self):
        return "%s (ynmp id %s)" % (self.constituency.name,
                                    self.ynmp_seat_id)
    
class Candidate(Model):
    ynmp_id = models.CharField(max_length=9)
    status = models.CharField(max_length=128,
                              null=True,
                              blank=True)
    email = models.CharField(max_length=128,
                             null=True,
                             blank=True)
    updated = models.CharField(max_length=64,
                               null=True,
                               blank=True)
    gender = models.CharField(max_length=10,
                              null=True,
                              blank=True)
    code = models.CharField(max_length=128,
                            null=True,
                            blank=True)
    university = models.CharField(max_length=250,
                                  null=True,
                                  blank=True)
    name = models.CharField(max_length=128,
                            null=True,
                            blank=True)
    phone = models.CharField(max_length=128,
                             null=True,
                             blank=True)
    dob = models.CharField(max_length=16,
                           null=True,
                           blank=True)
    ynmp_party_id = models.CharField(max_length=64,
                                     null=True,
                                     blank=True)
    party = models.ForeignKey(Party,
                              null=True,
                              blank=True)
    

class Candidacy(Model):
    ynmp_id = models.CharField(max_length=9,
                               blank=True,
                               null=True)
    ynmp_constituency = models.ForeignKey(YNMPConstituency)
    candidate = models.ForeignKey(Candidate)

    def __unicode__(self):
        return "%s standing for %s in %s" % (self.candidate.name,
                                             self.candidate.party.name,
                                             self.ynmp_constituency.constituency.name)

class YNMPAction(Model):
    user = models.ForeignKey(CustomUser)
    points_awarded = models.IntegerField()
    task = models.CharField(max_length=32)
    summary = models.TextField(null=True)
    date = models.DateTimeField(auto_now_add=True)
    candidate_code = models.CharField(max_length=80) # Lengths from YNMP code
    candidate_name = models.CharField(max_length=200)
    party_name = models.CharField(max_length=80)
    details_added = models.TextField(null=True)
    
    def __unicode__(self):
        return "%s did %s (%s) getting %d points" % (self.user,
                                                     self.task,
                                                     self.summary,
                                                     self.points_awarded)

    @property
    def action_text(self):
        if self.task == "bad_details": # User is adding contact info
            details = self.details_added.split(",")

            added_text = "added "
            first = True
            i = 1
            for detail in details:
                if first:
                    first = False
                elif i == len(details):
                    added_text += ", and "
                else:
                    added_text += ", "
                added_text += expand_item(detail)
                i += 1

            return added_text
        else:
            return "Summat"

"""
    YNMP supplies:

    dc_user_id
    points_awarded
    summary
    task
    candidate_code
    candidate_id
    candidate_name
    party_name
    details_added
"""
