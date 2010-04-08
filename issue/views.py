from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required

from signup.models import Constituency
from models import RefinedIssue, Issue, make_league_table
from models import ConstituencyIssueCompletion
from tasks.util import login_key
from forms import AddIssueForm, ModerateIssueForm
from utils import addToQueryString

import settings

import signals
import datetime
import csv

def issues(request, constituency):
    year = settings.CONSTITUENCY_YEAR
    c = Constituency.objects.get(slug=constituency,
                                     year=year)
    return render_to_response("issues/issues.html",
                              {'constituency': c,},
                              context_instance=RequestContext(request))

@login_key
@login_required
def add_issue(request, constituency=None, submitted=False):
    if constituency:
        year = settings.CONSTITUENCY_YEAR
        c = Constituency.objects.get(slug=constituency,
                                     year=year)
    else:
        c = None
    issues = Issue.objects.filter(constituency=c)\
             .order_by('-created_at')
                                     
    vars = {'constituency': c,
            'submitted': submitted,
            'issues': issues
            }

    if request.method == "POST":
        add_issue_form = AddIssueForm(request.POST,
                                      request.FILES,
                                      user=request.user)
        if add_issue_form.is_valid():
            issue = add_issue_form.save(constituency=c)
            signals.issue_added.send(None,
                                     user=request.user,
                                     issue=issue,
                                     constituency=c)
            return HttpResponseRedirect(reverse('add_issue_thanks',
                                        kwargs={'constituency':c.slug}))
        else:
            vars['form'] = add_issue_form
    else:
        vars['form'] = AddIssueForm(user=request.user)
    return render_to_response("add_issue.html", vars,
                              context_instance=RequestContext(request))

@login_required
@permission_required('issue.change_issue')
def moderate_issue(request):
    moderate_issue_form = None
    if request.method == "POST":
        issue = Issue.objects.get(pk=request.POST['id'])
        # issue.question = request.POST['question'] Don't modify original issue
        # issue.reference_url = request.POST['reference_url']
        found = False
        for k in request.POST.keys():
            if k.startswith("Hide"):
                issue.status = k.lower()
                notice = ("Issue hidden, thank you! Here's another "
                          "issue to moderate.")
                found = True
        
        if not found and 'Approve' in request.POST:
            issue.status = 'approved'
            
            question = request.POST['question']
            reference_url = request.POST['reference_url']
            
            new_issue = RefinedIssue.objects.create(question=question,
                                                    reference_url=reference_url,
                                                    constituency=issue.constituency,
                                                    moderator=request.user,
                                                    based_on=issue
                                                    )
            notice = "Issue moderated, thank you! Here's another issue to moderate."
        elif not found:
            raise Exception("No known button submitted in form data")

        completion = issue.constituency.issue_completion.get()
        completion.calculate_completion()
        issue.last_updated_by = request.user
        issue.save()

        signals.issue_moderated.send(None, user=request.user, issue=issue)
        return HttpResponseRedirect(addToQueryString(reverse('moderate_issue'), 
                                                     {'notice' : notice}))
    else:
        issue_list = Issue.objects\
                     .filter(status='new',
                             constituency__issue_completion__completed=False)\
                     .order_by('constituency__issue_completion__number_to_completion')\
                     .distinct()
        if issue_list.count() == 0:
            return HttpResponseRedirect(addToQueryString("/", 
                { 'notice' : "Every issue has now been moderated! Thank you for helping." }))
        issue = issue_list[0]

    if moderate_issue_form == None:
        moderate_issue_form = ModerateIssueForm(instance = issue)

    vars = { }
    vars['issue'] = issue
    vars['form'] = moderate_issue_form
    vars['issues'] = Issue.objects.filter(constituency=issue.constituency).order_by('-created_at')
    vars['hidden_issues'] = Issue.hidden_objects.filter(constituency=issue.constituency).order_by('-created_at')
    vars['constituency'] = issue.constituency

    vars['done'] = RefinedIssue.objects.all().count()
    vars['missing'] = issue_list.count()
    vars['total'] = vars['done'] + vars['missing']
    vars['percentage'] = float(vars['done']) / float(vars['total']) * 100

    vars['league_table_all_time'] = make_league_table()
    one_week_ago = datetime.datetime.now() - datetime.timedelta(7)
    vars['league_table_this_week'] = make_league_table(Issue.all_objects.filter(updated_at__gt=one_week_ago).all())

    return render_to_response("moderate_issue.html", vars,
                              context_instance=RequestContext(request))

# Export CSV file of all refined issues (initially made for loading 
# into TheyWorkForYou survey)
def refined_csv(request):
    refined_local_issues = RefinedIssue.objects.all()

    response = HttpResponse(mimetype='text/csv')
    response['Content-Disposition'] = 'attachment; filename=refined_local_issues.csv'

    writer = csv.writer(response)
    for i in refined_local_issues: 
        writer.writerow([i.id, i.question.encode('utf-8'), i.reference_url.encode('utf-8'), i.constituency.name.encode('utf-8'), 
            i.created_at.strftime("%Y-%m-%dT%H:%M:%S"), i.updated_at.strftime("%Y-%m-%dT%H:%M:%S")])

    return response



