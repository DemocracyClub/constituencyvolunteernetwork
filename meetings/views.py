import re

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

from signup.views import render_with_context
from tasks.util import login_key

from models import MeetingInterest
import signals

@login_key
@login_required
def express_interest(request, constituency_slug=None):
    """ Report the addition of a leaflet """  
    context = {}
    interest = None
    if request.method == "POST":
        if request.POST.get('interest', False):
            interest = MeetingInterest.objects\
                       .create(user=request.user,
                               postcode=request.POST['postcode'])
            signals.interest_expressed.send(None, user=request.user)
        elif request.POST.get('organise', False):
            interest = MeetingInterest.objects\
                       .create(user=request.user,
                               organiser=True,
                               postcode=request.POST['postcode'])
            signals.interest_expressed.send(None, user=request.user)

        context['interest'] = interest
        return render_with_context(request, 'thanks.html', context)
    return render_with_context(request, 'express_interest.html', context)
