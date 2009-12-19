from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

import signup.views
from signup.views import render_with_context

import signals

def add(request, login_key=None):
    """ Report the addition of a leaflet """
    if login_key is not None:
        # should we generate separate login keys for each taskuser for security?
        signup.views.do_login(request, login_key)
    
    if not request.user.is_authenticated():
	return HttpResponseRedirect(reverse('home'))
    
    # Emit signal. Intercepted by the task.py code
    signals.leaflet_added.send(None, user=request.user)

    return HttpResponseRedirect(reverse('welcome'))