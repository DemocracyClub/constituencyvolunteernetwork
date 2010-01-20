from urllib import quote

from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

from django.contrib.sites.models import Site

from forms import InviteForm
from signup.views import render_with_context
from utils import addToQueryString

@login_required
def index(request):
    vars = {}
    if request.method == "POST":
        invite_form = InviteForm(request.POST, request.FILES)
        if invite_form.is_valid():
            invite_form.save(request.user)
            context = {'notice':'Thanks for inviting more people to join!'}
            return HttpResponseRedirect(addToQueryString(reverse('tasks'),
                                                         context))
        else:
            vars['invite_form'] = invite_form
    else:
        vars['invite_form'] = InviteForm()
        
    vars['siteurl'] = quote("http://%s" % Site.objects.get_current().domain)
    request.user.seen_invite = True
    request.user.save()    
    return render_with_context(request,
                               "invite/invite_page.html",
                               vars)

