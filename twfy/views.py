import logging
import urllib
import math

from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.db.models import aggregates,sql
from django.db.models import Avg, Count, StdDev
from django.views.decorators.cache import cache_page
from django.core.urlresolvers import reverse

from signup.util import render_with_context
from models import SurveyInvite
from models import Statement
from models import SurveyResponse
from signup.models import Constituency
from ynmp.models import Party
from ynmp.models import Candidacy
from signup.views import _add_candidacy_data
from signals import pester_action_done

import settings

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

@cache_page(60*60)
def parties(request):
    context = {}
    statements = []
    #for party in Party.objects.all():
    #    data = {}
    #    statements =
    #    Statement.objects.filter(national=True).annotate(agreement=Avg('surveyresponse__agreement'))
    chart = ""
    for statement in Statement.objects.filter(national=True):
        bottoms = []
        boxbottoms = []
        boxtops = []
        tops = []
        parties = Party.objects.annotate(count=Count('candidate'))\
                  .filter(count__gt=200)
        something = False
        for party in parties:
            responses = SurveyResponse.objects\
                        .filter(candidacy__candidate__party=party,
                                statement=statement)
            avg = responses.aggregate(avg=Avg('agreement'))['avg']
            stddev = responses.aggregate(stddev=StdDev('agreement'))['stddev']
            if responses.count():
                error = stddev/math.sqrt(responses.count()-1)
            else:
                error = None
            if error:
                something = True
                bottoms.append(str(int(avg - stddev)))
                boxbottoms.append(str(int(avg - 1)))
                boxtops.append(str(int(avg + 1)))
                tops.append(str(int(avg + stddev)))            
                party.avg = avg
                party.stddev = stddev
                party.error = error
            else:
                bottoms.append("")
                boxbottoms.append("")
                boxtops.append("")
                tops.append("")
                party.avg = ""
                party.stddev = ""
                party.error = ""
        chart = "http://chart.apis.google.com/chart?chs=800x125&cht=lc&chd=t0:"
        chart += ",".join(bottoms)
        chart += "|"
        chart += ",".join(boxbottoms)
        chart += "|"
        chart += ",".join(boxtops)
        chart += "|"
        chart += ",".join(tops)
        chart += "&chm=F,0000FF,0,,20&chxt=x,y&chxl=0:|"
        chart += "|".join([urllib.quote_plus("".join([y[0] for y in x.name.split(" ")])) for x in parties])
        if something:
            statements.append({'parties':parties,
                               'statement':statement,
                               'chart':chart})
        
    context['statements'] = statements
    context['chart'] = chart
    return render_with_context(request,
                               'parties.html',
                               context)

@login_required
def pester(request, constituency):
    if not request.user.is_superuser:
        # turned off once election has started
        return HttpResponseRedirect(
            reverse('home'))

    context = {}
    constituency = Constituency.objects.get(pk=constituency)
    context['constituency'] = constituency
    count = SurveyInvite.objects.filter(filled_in=True).count()
    context['total_count'] = count
    context = _add_candidacy_data(context, constituency)
    if context['contacted'].count() == 1:
        context['one_left'] = True
        if context['contacted'][0].candidate.party.name == "Conservative Party":
            context['one_tory_left'] = True            
    if request.GET.has_key('pester'):
        email_candidacies = []
        no_email_candidacies = []
        key = 'candidacy_'
        for k, v in request.GET.items():
            if k.startswith(key):
                candidacy = Candidacy.objects.get(
                    pk=k[len(key):],
                    ynmp_constituency__constituency=constituency)
                if candidacy.candidate.email:
                    email_candidacies.append(candidacy)
                else:
                    no_email_candidacies.append(candidacy)
        context['email_candidacies'] = email_candidacies
        context['no_email_candidacies'] = no_email_candidacies
    default_msg = "Dear candidates,\n\n\n\n\nYours,\n%s\n%s"
    if request.user.is_anonymous():
        user_email = request.session.get('email', '')
        user_name = request.session.get('name', '')
        user_postcode = request.session.get('postcode', '')
    else:
        user_email = request.user.email
        user_name = "%s %s" % (request.user.first_name,
                               request.user.last_name)
        user_postcode = request.user.postcode
    default_msg = default_msg % (user_name, user_postcode)
    context['message'] = default_msg
    context['user_email'] = user_email
    if request.method == "POST":
        if request.POST.has_key('finished'):
            return render_with_context(request,
                                       'pester_thanks.html',
                                       context)            
        candidacies = []
        for key in request.POST.getlist('candidacy'):
            candidacy = Candidacy.objects.get(
                pk=int(key),
                ynmp_constituency__constituency=constituency)
            candidacies.append(candidacy)
        subject = request.POST.get('subject','').strip()
        message = request.POST['message'].strip()
        mfrom = request.POST.get('mfrom','').strip()
        debug_to = request.POST.get('debug_to','').strip()
        if not subject:
            context['subject'] = subject
            context['message'] = message
            context['mfrom'] = mfrom
            context['error'] = "You must give the email a subject"
        else:

            if not user_email:
                user_email = request.POST.get('mfrom', 'unknown')
            sbj = "[ NONE ]"
            msg = ""
            for candidacy in candidacies:
                # calculate the login link
                quiz_url = "http://election.theyworkforyou.com/survey/"
                token = candidacy.surveyinvite_set.get().survey_token
                quiz_url += token
                quiz_words = "To start the survey, please visit %s" % quiz_url
                msg = ("This is a message from a voter in your "
                       "constituency about the TheyWorkForYou "
                       "survey. " + quiz_words + "\n"
                       "----------\n\n") + message
                if user_email != "unknown":
                    msg = msg + "\n\n-----------\n\nNOTE: you can write to this voter at <"\
                          +user_email+\
                          ">, but please be sure not to send them the survey link when you do so."
                msg = msg + ("\n\n"
                             "-----------\n" + quiz_words)
                mfrom = "quiz@democracyclub.org.uk"
                if settings.DEBUG:
                    sbj = "%s to %s" % (subject,
                                        candidacy.candidate.email)
                else:
                    sbj = subject
                if settings.DEBUG:
                    mto = debug_to
                else:
                    mto = candidacy.candidate.email
                send_mail(sbj,
                          msg,
                          mfrom,
                          [mto])
            send_mail("[%s] %s" % (constituency.slug,
                                   sbj),
                      "From: %s\n\n%s" % (user_email, msg),
                      mfrom,
                      ['hassle@democracyclub.org.uk'])
            if not request.user.is_anonymous():
                pester_action_done.send(None, user=request.user)
            for candidacy in candidacies:
                invite = candidacy.surveyinvite_set.get()
                invite.pester_emails_sent += 1
                invite.save()
            # onto thankyou page
            if no_email_candidacies:
                return render_with_context(request,
                                           'pester2.html',
                                           context)
            else:
                return render_with_context(request,
                                           'pester_thanks.html',
                                           context)
        
    return render_with_context(request,
                               'pester.html',
                               context)
    
