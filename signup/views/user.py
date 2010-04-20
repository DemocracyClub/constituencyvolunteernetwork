from django.contrib.auth import logout
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required

from signup.forms import EditUserForm
from signup.models import CustomUser
from signup.models import RegistrationProfile 
from signup.models import Constituency
from utils import addToQueryString
from signup.util import render_with_context, key_login

def do_login(request, key):
    context = key_login(request, key)
    
    return HttpResponseRedirect(addToQueryString("/", context))

def do_logout(request):
    logout(request)
    return HttpResponseRedirect("/")

def unsubscribe(request, key):
    profile = RegistrationProfile.objects.get_user(key, only_activated=False)
    
    error = notice = ""
    if RegistrationProfile.objects.deactivate_user(profile,
                                                   user_request=True):
        logout(request)            
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

def all_users(request, slug=None):
    context = {}
    constituency = get_object_or_404(Constituency, slug=slug)
    users = constituency.customuser_set.all()
    context['users'] = users
    context['constituency'] = constituency
    if request.user.is_authenticated():
        context['show_email'] = \
            bool(request.user.constituencies\
                 .filter(id=constituency.id))
    else:
        context['show_email'] = False

    return render_with_context(request,
                               'all_users.html',
                               context)


@login_required
def edit_user(request, id):
    id = int(id)
    if request.user.id != id and not request.user.has_perm("signup.edit_customuser"):
        return HttpResponse(status=403)
    else:    
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
            # we assume that if they previously unsubscribed, they've
            # now changed their minds
            user.unsubscribed = False
            user.save()
            profile = user.registrationprofile_set.get()
            profile.send_activation_email()
            messages.append("Activation email re-sent. Please check your %s inbox. If it isn't there, check your spam folders" % email)
    context = {'messages':messages}
    return render_with_context(request,
                               "email_reminder.html",
                               context) 
