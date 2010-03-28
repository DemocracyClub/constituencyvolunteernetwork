from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views

###############################################################################
urlpatterns = patterns('tsc',
        url(r'^add/(?P<constituency_slug>[\w-]+)/(?P<login_key>[\w-]+)$',
        views.add,
        name="tsc_add"),

        url(r'^add/(?P<constituency_slug>[\w-]+)/$',
        views.add,
        name="tsc_add"),

        url(r'^add/$',
        views.add,
        name="tsc_add"),

        url(r'^start/(?P<constituency_slug>[\w-]+)/$',
        views.start,
        name="tsc_start"),

        url(r'^test$',
            direct_to_template,
            {'template':'tsc_test.html'},
            name="tsc_test"),
)
