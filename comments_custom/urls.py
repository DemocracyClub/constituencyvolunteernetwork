from django.conf.urls.defaults import *
import views


###############################################################################
urlpatterns = patterns('comments_custom',
    url(r'^delete/(\d+)/(.*)/$', views.delete, name="custom_comment_delete"),
)
