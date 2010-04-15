from django.conf.urls.defaults import *

import views

################################################################################
urlpatterns = patterns('twfy',
    url(r'^chart/$', views.chart, name="chart"),
)
