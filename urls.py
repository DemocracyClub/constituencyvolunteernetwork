from django.conf.urls.defaults import *
from settings import MEDIA_ROOT
from django.views.static import serve
from issue.feeds import AllIssues

import signup

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

feeds = {
    'allissues': AllIssues,
    }

urlpatterns = patterns('',
    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enablese admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    (r'^media/(?P<path>.*)$', serve,
     {'document_root': MEDIA_ROOT,
      'show_indexes': True}),
    ('^invite/', include('invite.urls')), 
    ('^tsc/', include('tsc.urls')),
    ('^tasks/', include('tasks.urls')),
    ('^issues/', include('issue.urls')),
    ('^s/', include('shorten.urls')),
    ('^meetings/', include('meetings.urls')),
    (r'^comments/core/', include('django.contrib.comments.urls')),
    (r'^comments/', include('comments_custom.urls')),
    (r'^ynmp/', include('ynmp.urls')),
    (r'^twfy/', include('twfy.urls')),
    ('^', include('signup.urls')),
    (r'^feeds/(?P<url>.*)/$', 'django.contrib.syndication.views.feed',
     {'feed_dict': feeds}),       
)
