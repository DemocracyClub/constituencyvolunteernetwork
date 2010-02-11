import re
from types import ListType

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import signup.views
from signup.views import render_with_context
from signup.models import Constituency
from tasks.util import login_key

from models import UploadedLeaflet
import signals

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
        c = Constituency.objects.get(slug=constituency_slug)

    for url in leaflet_urls:
        UploadedLeaflet.objects.create(url=url,
                                       user=request.user,
                                       constituency=c)

        signals.leaflet_added.send(None, user=request.user, constituency=c)
    if leaflet_urls:
        return HttpResponseRedirect(reverse('tasks'))
    else:
        return render_with_context(request, 'tsc/add.html', context)

