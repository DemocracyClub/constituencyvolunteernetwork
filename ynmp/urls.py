from django.conf.urls.defaults import *

import views

################################################################################
urlpatterns = patterns('ymmp',
    url(r'^api$', views.api, name="api"),
)
