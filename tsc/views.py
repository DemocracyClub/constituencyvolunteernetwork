from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

import signup.views
from signup.views import render_with_context
from tasks.util import login_key

from models import UploadedLeaflet
import signals

@login_key
@login_required
def add(request):
    """ Report the addition of a leaflet """  
    context = {}
    
    if 'leaflet_url' in request.POST:
        # Emit signal. Intercepted by the task.py code
        uploaded_leaflet = \
            UploadedLeaflet.objects.create(url=request.POST['leaflet_url'],
                                           user=request.user)                                           
        
        signals.leaflet_added.send(None, user=request.user)
        context['message'] = "Thanks for adding a leaflet. You can add another one if you want or <a href='/tasks/upload-leaflet'>go back to the task</a>"

    return render_with_context(request, 'tsc/add.html', context)