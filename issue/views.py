from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from signup.models import Constituency
from models import Issue
from task import task_slug
from tasks.util import login_key
from forms import AddIssueForm
import signals

@login_key
@login_required
def add_issue(request, constituency=None, submitted=False):
    if constituency:
        c = Constituency.objects.get(slug=constituency)
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
    return render_to_response("add_issue.html",
                              vars,
                              context_instance=RequestContext(request))



