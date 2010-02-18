from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

import settings

def navigation(context):
    context = {'pages': FlatPage.objects.all(),
               'needs_activation': (not context.user.is_anonymous()) and (not context.user.is_active),}

    return context

def current_site(context):
    context = {'current_site': Site.objects.get_current()}
    return context

def google_analytics(context):    
    context = {'google_analytics_id': settings.GOOGLE_ANALYTICS_ID}
    return context
