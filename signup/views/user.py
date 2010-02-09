from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.auth.decorators import login_required

from signup.forms import EditUserForm
from signup.models import CustomUser, RegistrationProfile
from signup.views import render_with_context
import signup.signals as signals

from utils import addToQueryString

def _login(request, profile):
    user = authenticate(username=profile.user.email)
    login(request, user)
    signals.user_login.send(None, user=user)

def do_login(request, key):
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
    
    return HttpResponseRedirect(addToQueryString("/", context))

def do_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def unsubscribe(request, key):
    profile = RegistrationProfile.objects.get_user(key, only_activated=False)
    
    error = notice = ""

    if RegistrationProfile.objects.deactivate_user(profile):
        notice = "Your user account has been deactivated and will no longer receive emails"
    else:
        error = "Invalid key"

    context = {'error': error,
               'notice': notice}
    
    return HttpResponseRedirect(addToQueryString("/", context))

def user(request, id):
    from tasks.models import TaskUser # Import here to avoid circular dependency
    
    context = {}
    user = get_object_or_404(CustomUser, pk=id)
    context['profile_user'] = user
    context['activity'] = TaskUser.objects.\
        filter(user=user).\
        filter(user__can_cc=True).\
        filter(state__in=[TaskUser.States.started,TaskUser.States.completed]).\
        order_by('-date_modified').distinct()
    context['badges'] = user.badge_set.order_by('-date_awarded')
    return render_with_context(request,
                               'user.html',
                               context)

@login_required
def edit_user(request, id):
    id = int(id)
    if request.user.id != id:# and not request.user.has_perm("signup.edit_customuser"):
        return HttpResponse(status=403)
    else:
        print "Rendering form"
    
        data = None
        user = CustomUser.objects.get(pk=id)
        
        if request.method == "POST":
            data = request.POST
        else:
            data = user.__dict__

        form = EditUserForm(user, data)

        notice = ""

        if request.method == "POST":
            if form.is_valid():
                user = form.save()
                notice = "User profile saved"
        
        context = {'form': form, 'edit_user': user, 'notice': notice,}

        return render_with_context(request, "user_edit.html", context)

def email_reminder(request):
    messages = []
    if request.method == "POST":
        email = request.POST['email']
        
        user = None
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.append("I couldn't find a user with email address %s" % email)
        else:
            profile = user.registrationprofile_set.get()
            profile.send_activation_email()
            messages.append("Activation email re-sent. Please check your %s inbox. If it isn't there, check your spam folders" % email)
    context = {'messages':messages}
    return render_with_context(request,
                               "email_reminder.html",
                               context) 
