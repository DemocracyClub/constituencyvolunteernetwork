from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views

################################################################################
urlpatterns = patterns('invite.views',
    url(r'^$', views.index, name="inviteindex"),
    url(r'^thankyou$$',
        direct_to_template,
        kwargs={'template':'invite/thankyou.html'},
        name="thankyou"),
)
