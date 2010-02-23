from django.conf.urls.defaults import *
import views, views.user, views.statistics
from django.views.generic.simple import direct_to_template
from tasks.views import home

################################################################################
urlpatterns = patterns('casestudies',
    url(r'^$', views.home, name="home"),
    url(r'^home2$', views.home2, name="home2"),
    url(r'^welcome$', home, name="welcome"),
    
    url(r'^users/(?P<id>[\w-]+)/$',
        views.user.user,
        name="user"),
    url(r'^users/(?P<id>[\w-]+)/edit$',
        views.user.edit_user,
        name="edit_user"),
    url(r'^login/(?P<key>\w+)/$',
        views.user.do_login,
        name="login"),
    url(r'^logout/$',
        views.user.do_logout,
        name="logout"),
    url(r'^reminder$',
        views.user.email_reminder,
        name="email_reminder"),
    url(r'^unsubscribe/(?P<key>\w+)/$',
        views.user.unsubscribe,
        name="unsubscribe"),
    
    url(r'^constituencies/$',
        views.constituencies,
        name="constituencies"),
    url(r'^constituencies/(?P<slug>[\w-]+)/$',
        views.constituency,
        name="constituency"),
    url(r'^constituencies/(?P<slug>[\w-]+)/(?P<year>\d+)/$',
        views.constituency,
        name="constituency-by-year"),
    url(r'^add_constituency/$',
        views.add_constituency,
        name="add_constituency"),
    url(r'^delete_constituency/(?P<slug>[\w-]+)/$',
        views.delete_constituency,
        name="delete_constituency"),

    url(r'^statistics/fewerthan/(?P<volunteers>\d+)/geo.rss$',
        views.statistics.constituencies_with_fewer_than_rss,
        name="constituencies_with_fewer_than_rss"),
    url(r'^statistics/morethan/(?P<volunteers>\d+)/geo.rss$',
        views.statistics.constituencies_with_more_than_rss,
        name="constituencies_with_more_than_rss"),
    url(r'^statistics/$',
        views.statistics.statistics,
        name="statistics"),
    url(r'^statistics/heatmap.svg$',
        views.statistics.generate_map_2010,
        name="map"),
    url(r'^statistics/(?P<date>[\w-]+)/heatmap.svg$',
        views.statistics.generate_map_2010,
        name="map_on_date"),
    url(r'^manage$',
        direct_to_template,
        {'template':'manage.html'},
        name="manage"),
                      
)
