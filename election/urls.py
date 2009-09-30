from django.conf.urls.defaults import *
from django.views.generic import list_detail
from django.db.models import Count

from election.models import Party, Candidate

from django.contrib import admin
admin.autodiscover()


parties_all = {
    "queryset" : Party.objects.annotate(candidate_count=Count("candidate__id")),
    "template_name": "party_list.html"
}

candidates_all = {
    "queryset" : Candidate.objects.all(),
    "template_name": "candidate_list.html"
}


urlpatterns = patterns('',
    (r'^parties/$', list_detail.object_list, parties_all),
    (r'^candidates/$', list_detail.object_list, candidates_all),
)
