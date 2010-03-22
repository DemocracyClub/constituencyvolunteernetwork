from django.conf.urls.defaults import *

import views

################################################################################
urlpatterns = patterns('ymmp',
    url(r'^api/$', views.api, name="ynmp_api"),
    url(r'^start/$', views.start, name="ynmp_start"),
)
