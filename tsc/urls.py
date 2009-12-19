from django.conf.urls.defaults import *
import views

###############################################################################
urlpatterns = patterns('tsc',
        url(r'^add/(?P<login_key>[\w-]+)$',
        views.add,
        name="task_add"),
)