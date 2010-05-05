from django.conf.urls.defaults import *

import views

################################################################################
urlpatterns = patterns('twfy',
    url(r'^chart/$',
        views.chart,
        name="chart"),
    url(r'^parties/$',
        views.parties,
        name="parties"),
    url(r'^remind/(?P<constituency>\w+)/$',
        views.pester,
        name="pester"),
)
