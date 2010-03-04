from django.db import models
from django.conf import settings

from tasks.models import Task
from signup.models import Constituency, CustomUser

import collections

STATUS_CHOICES = (
    ('new', 'New'),
    ('approved', 'Approved'),
    ('hide-notlocal', 'Hide - not local'),
    ('hide-toogeneral', 'Hide - too general'),
    ('hide-nopolicy', 'Hide - no clear policy'),
    ('hide-other', 'Hide - other'),
)

class VisibleIssuesManager(models.Manager):
    def get_query_set(self):
        return super(VisibleIssuesManager, self).get_query_set().exclude(status='hide')

class HiddenIssuesManager(models.Manager):
    def get_query_set(self):
        return super(HiddenIssuesManager, self).get_query_set().filter(status='hide')

class Issue(models.Model):
    question = models.TextField()
    reference_url = models.URLField(max_length=2048, # reasonable maximum: http://www.boutell.com/newfaq/misc/urllength.html
                                    blank=True,
                                    null=True) 
    constituency = models.ForeignKey(Constituency)
    created_by = models.ForeignKey(CustomUser)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    status = models.CharField(max_length=20,
                              choices=STATUS_CHOICES,
                              default='new')

    last_updated_by = models.ForeignKey(CustomUser,
                                        null=True,
                                        related_name='issues_last_updater')

    def __unicode__(self):
        return self.question

    class Meta:
        get_latest_by = 'created_at'

    # override default manager so results don't show hidden objects by default
    objects = VisibleIssuesManager() 
    hidden_objects = HiddenIssuesManager()
    all_objects = models.Manager() # visible and hidden ones

class RefinedIssue(models.Model):
    question = models.TextField()
    reference_url = models.URLField(max_length=2048, # reasonable maximum: http://www.boutell.com/newfaq/misc/urllength.html
                                    blank=True,
                                    null=True) 
    constituency = models.ForeignKey(Constituency)
    based_on = models.ForeignKey(Issue, related_name="refined")
    moderator = models.ForeignKey(CustomUser, related_name="moderated_issues")

    def __unicode__(self):
        return "%s based on issue by %s" % (self.question, self.based_on.created_by)

def make_league_table(issues = None):
    if not issues:
        issues = Issue.all_objects.all()

    table = collections.defaultdict(lambda: 0)
    for issue in issues:
        user = issue.last_updated_by
        if user:
            table[user] += 1

    league_table = []
    for user, count in table.iteritems():
        league_table.append((user, count))
    league_table.sort(lambda a,b: cmp(b[1],a[1]))

    return league_table

    
