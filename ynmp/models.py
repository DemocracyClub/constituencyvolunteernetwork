from django.db import models

from tasks.models import Task
from signup.models import Model, CustomUser

def expand_item(word):
    words = {'email': 'an email address',
             'phone': 'a phone number',
             'fax': 'a fax number',
             'address': 'a postal address',}
    return words[word]

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
