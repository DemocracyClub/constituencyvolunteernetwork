try:
    import json
except ImportError:
    import simplejson as json
from itertools import chain

from django.http import HttpResponse, HttpResponseBadRequest
from django.http import HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from signup.models import CustomUser
from signup.util import render_with_context
from models import SurveyInvite
from ynmp.models import Party

from django.db.models import aggregates,sql
class CountIf(sql.aggregates.Count):
    sql_template = '%(function)s(CASE WHEN %(field)s=%(equals)s THEN 1 ELSE 0 END)'
sql.aggregates.CountIf = CountIf



def chart(request):
    context = {}
    context['invites'] = SurveyInvite.objects.all()
    invites_sent = aggregates.Count(
        'candidate__candidacy__surveyinvite__emailed',
        equals=True)
    invites_sent.name = 'CountIf'
    replies_received = aggregates.Count(
        'candidate__candidacy__surveyinvite__filled_in',
        equals=True)
    replies_received.name = 'CountIf'
    parties = Party.objects.all()\
              .filter(candidate__candidacy__surveyinvite__emailed=True)\
              .annotate(invites_sent=invites_sent)\
              .distinct()\
              .order_by('-invites_sent')
    for party in parties:
        party.replies_received = SurveyInvite.objects\
                                 .filter(filled_in=True,
                                         candidacy__candidate__party=party)\
                                         .count()

    parties = list(parties[:15])
    parties.sort(lambda x, y: cmp(float(y.replies_received)/y.invites_sent,
                                  float(x.replies_received)/x.invites_sent))
    context['parties'] = parties
    return render_with_context(request,
                               'chart.html',
                               context)

