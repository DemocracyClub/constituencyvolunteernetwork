import re
from types import ListType

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import signup.views
from signup.views import render_with_context
from tasks.util import login_key

from models import UploadedLeaflet
import signals

url_regex = re.compile(ur'http://www.thestraightchoice.org/leaflet.php?q=(\d+)', re.U)

@login_key
@login_required
def add(request):
    """ Report the addition of a leaflet """  
    context = {}
    leaflet_urls = request.GET.getlist('leaflet_url') \
                   or request.POST.getlist('leaflet_url')
    
    for url in leaflet_urls:
        UploadedLeaflet.objects.create(url=url,
                                       user=request.user)
        signals.leaflet_added.send(None, user=request.user)
    if leaflet_urls:
        return HttpResponseRedirect(reverse('tasks'))
    else:
        return render_with_context(request, 'tsc/add.html', context)

