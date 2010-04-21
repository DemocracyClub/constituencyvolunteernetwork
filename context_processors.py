from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

from signup.models import RegistrationProfile
import settings

def navigation(context):
    needs_activation = False
    if not context.user.is_anonymous():
        try:
            profile = context.user.registrationprofile_set.get()
            if not profile.activated:
                needs_activation = True
        except RegistrationProfile.DoesNotExist:
            pass
    context = {'pages': FlatPage.objects.all().order_by('id'),
               'needs_activation': needs_activation}

    return context

def current_site(context):
    context = {'current_site': Site.objects.get_current()}
    return context

def google_analytics(context):    
    context = {'google_analytics_id': settings.GOOGLE_ANALYTICS_ID}
    return context

def is_debug(context):    
    context = {'DEBUG': settings.DEBUG}
    return context
