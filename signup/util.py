from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render_to_response
from signup.models import RegistrationProfile 
import signals

def _login(request, profile):
    user = authenticate(username=profile.user.email)
    login(request, user)
    signals.user_login.send(None, user=user)

def key_login(request, key):
    profile = RegistrationProfile.objects.get_user(key, only_activated=False)

    error = notice = ""

    if not profile:
        error = "Sorry, that key was invalid"
    elif not profile.activated:
        if not RegistrationProfile.objects.activate_user(profile):
            error = "Sorry, that key was invalid"
        else:
            notice = "Thank you for confirming your email address"
            _login(request, profile)
    else:
        _login(request, profile)
    
    context = {'error': error,
               'notice': notice}
    
    return context

def render_with_context(request,
                        template,
                        context,
                        **kw):
    kw['context_instance'] = RequestContext(request)
    return render_to_response(template,
                              context,
                              **kw)
