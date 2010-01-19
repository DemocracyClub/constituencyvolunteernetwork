from signup.models import CustomUser, RegistrationProfile
from signup.views import render_with_context

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
        
    return render_with_context(request, "email_reminder.html", {})
