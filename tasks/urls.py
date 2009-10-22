from django.conf.urls.defaults import *
import views

################################################################################
urlpatterns = patterns('tasks',
    url(r'^tasks/$', views.home, name="home"),
    url(r'^tasks/(?P<slug>[\w-]+)/$',
        views.task,
        name="task"),
    url(r'^tasks/(?P<slug>[\w-]+)/start/$',
        views.start_task,
        name="start_task"),
    url(r'^tasks/(?P<slug>[\w-]+)/complete/$',
        views.complete_task,
        name="complete_task"),
    url(r'^tasks/(?P<slug>[\w-]+)/ignore/$',
        views.ignore_task,
        name="ignore_task"),
    url(r'^tasks/(?P<slug>[\w-]+)/unignore/$',
        views.unignore_task,
        name="unignore_task"),
    url(r'^tasks/(?P<slug>[\w-]+)/(?P<login_token>[\w-]+)$',
        views.task,
        name="task_login"),
)

