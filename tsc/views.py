import re

from django.contrib.auth.decorators import login_required
import signals

import signup.views
from signup.views import render_with_context
from signup.models import Constituency
from tasks.util import login_key
import settings
from models import UploadedLeaflet

url_regex = re.compile(ur'http://www.thestraightchoice.org/leaflet.php?q=(\d+)', re.U)

@login_key
@login_required
def add(request, constituency_slug=None):
    """ Report the addition of a leaflet """  
    context = {}
    leaflet_urls = request.GET.getlist('v1') \
                   or request.POST.getlist('v1')

    c = None
    if constituency_slug:
        year = settings.CONSTITUENCY_YEAR
        c = Constituency.objects.get(slug=constituency_slug,
                                     year=year)
    else:
        c = request.user.home_constituency
    
    leaflet = None
    for url in leaflet_urls:
        leaflet = UploadedLeaflet.objects.create(url=url,
                                       user=request.user,
                                       constituency=c)

        signals.leaflet_added.send(None, user=request.user, constituency=c)
    if leaflet:
        # return HttpResponseRedirect(reverse('tasks'))
        context['constituency'] = c
        context['leaflet'] = leaflet
        return render_with_context(request, 'tsc/thanks.html', context)
    else:
        return render_with_context(request, 'tsc/add.html', context)

