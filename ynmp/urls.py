from django.conf.urls.defaults import *

import views

################################################################################
urlpatterns = patterns('ynmp',
    url(r'^api/$', views.api, name="ynmp_api"),
    url(r'^table/$', views.table, name="ynmp_table"),
    url(r'^start/(?P<login_key>[\w-]+)$',
        views.start,
        name="ynmp_start"),
)
