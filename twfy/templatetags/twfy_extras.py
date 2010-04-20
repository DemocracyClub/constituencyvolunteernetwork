from django import template

from signup.models import Constituency
from twfy.models import SurveyInvite


register = template.Library()

@register.simple_tag       
def party_count(constituency):
    constituency = Constituency.objects.get(pk=constituency)
    si = SurveyInvite.objects.filter(
        filled_in=True,
        candidacy__ynmp_constituency__constituency=constituency)
    return si.count()
