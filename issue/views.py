from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required, permission_required

from signup.models import Constituency, CustomUser
from models import Issue
from task import task_slug
from tasks.util import login_key
from forms import AddIssueForm, ModerateIssueForm
from utils import addToQueryString

import signals
import settings

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
        issue.question = request.POST['question']
        issue.reference_Url = request.POST['reference_url']

        if 'Hide' in request.POST:
            issue.status = 'hide'
            notice = "Issue hidden, thank you! Here's another issue to moderate."
        elif 'Approve' in request.POST:
            issue.status = 'approved'
            notice = "Issue moderated, thank you! Here's another issue to moderate."
        else:
            raise Exception("No known button submitted in form data")

        issue.last_updated_by = CustomUser.objects.get(user_ptr=request.user) # XXX how should this be done?
        issue.save()

        signals.issue_moderated.send(None, user=request.user, issue=issue)
        return HttpResponseRedirect(addToQueryString(reverse('moderate_issue'), { 'notice' : notice}))
    else:
        issue_list = Issue.objects.filter(status='new').order_by('?')[:1]
        if len(issue_list) == 0:
            return HttpResponseRedirect(addToQueryString("/", { 'notice' : "Every issue has now been moderated! Thank you for helping." }))
        issue = issue_list[0]

    if moderate_issue_form == None:
        moderate_issue_form = ModerateIssueForm(instance = issue)

    vars = { }
    vars['issue'] = issue
    vars['form'] = moderate_issue_form
    vars['issues'] = Issue.objects.filter(constituency=issue.constituency).order_by('-created_at')
    vars['hidden_issues'] = Issue.hidden_objects.filter(constituency=issue.constituency).order_by('-created_at')
    vars['constituency'] = issue.constituency

    vars['done'] = Issue.all_objects.exclude(status='new').count()
    vars['total'] = Issue.all_objects.count()
    vars['missing'] = vars['total'] - vars['done']
    vars['percentage'] = float(vars['done']) / float(vars['total']) * 100

    return render_to_response("moderate_issue.html", vars,
                              context_instance=RequestContext(request))



