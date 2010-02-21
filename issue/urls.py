from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template
import views

################################################################################
urlpatterns = patterns('issue.views',
    url(r'^add$',
        views.add_issue,
        name="add_issue"),
    url(r'^add/(?P<login_key>[\w-]+)$',
        views.add_issue,
        name="add_issue"), 
    url(r'^constituency/(?P<constituency>[\w-]+)/add$',
        views.add_issue,
        name="add_issue"),
    url(r'^constituency/(?P<constituency>[\w-]+)/add/(?P<login_key>[\w-]+)$',
        views.add_issue,
        name="add_issue"), 
    url(r'^constituency/(?P<constituency>[\w-]+)/$',
        views.issues,
        name="issues_page"),

    url(r'^moderate$',
        views.moderate_issue,
        name="moderate_issue"),

    url(r'^add/thanks$',
        views.add_issue,
        kwargs={'submitted':True},
        name="add_issue_thanks"),                     
    url(r'^add/(?P<constituency>[\w-]+)/thanks$',
        views.add_issue,
        kwargs={'submitted':True},
        name="add_issue_thanks"),                     
)

