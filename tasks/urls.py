from django.conf.urls.defaults import *
import views


###############################################################################
urlpatterns = patterns('tasks',
    url(r'^$', views.home, name="tasks"),
    url(r'^(?P<slug>[\w-]+)/start/(?P<login_key>[\w-]+)$',
        views.start_task,
        name="start_task"),
    url(r'^(?P<slug>[\w-]+)/start$',
        views.start_task,
        name="start_task"),
    url(r'^(?P<slug>[\w-]+)/complete/$',
        views.complete_task,
        name="complete_task"),
    url(r'^(?P<slug>[\w-]+)/ignore/$',
        views.ignore_task,
        name="ignore_task"),
    url(r'^(?P<slug>[\w-]+)/unignore/$',
        views.unignore_task,
        name="unignore_task"),
    url(r'^(?P<slug>[\w-]+)/(?P<login_key>[\w-]+)$',
        views.task,
        name="task"),
    url(r'^(?P<slug>[\w-]+)$',
        views.task,
        name="task"),
)
