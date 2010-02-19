from django.conf.urls.defaults import *
import views

urlpatterns = patterns('meetings',
        url(r'^interest/$',
        views.express_interest,
        name="express_interest"),
        url(r'^interest/(?P<login_key>[\w-]+)$',
        views.express_interest,
        name="express_interest"),

)
