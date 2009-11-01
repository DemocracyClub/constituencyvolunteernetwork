import types
import time
from itertools import chain

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.utils.safestring import SafeUnicode
from django.contrib.sites.models import Site

import models
from models import CustomUser, Constituency, RegistrationProfile
from forms import UserForm

from utils import addToQueryString
import settings

import geo

def render_with_context(request,
                        template,
                        context,
                        **kw):
    kw['context_instance'] = RequestContext(request)
    return render_to_response(template,
                              context,
                              **kw)

def home(request):
    context = {}
    year = settings.CONSTITUENCY_YEAR
    constituencies = Constituency.objects.filter(year=year)
    volunteers = CustomUser.objects.filter(is_active=True)
    count = volunteers.aggregate(Count('constituencies',
                                       distinct=True)).values()[0]
    total = constituencies.count()
    
    context['volunteers'] = volunteers.count()
    context['total'] = total
    context['count'] = count
    if total:
        context['percent_complete'] = int(float(count)/total*100)
    else:
        context['percent_complete'] = 0
    if request.method == "POST":
        form = UserForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save()
            user = authenticate(username=profile.user.email)
            login(request, user)
            return HttpResponseRedirect(reverse('welcome'))
        else:
            context['form'] = form
    else:
        context['form'] = UserForm()
    return render_with_context(request,
                               'home.html',
                               context)
                               
@login_required
def delete_constituency(request, slug):
    c = Constituency.objects.get(slug=slug)
    request.user.constituencies.remove(c)
    request.user.save()
    return HttpResponseRedirect(reverse('add_constituency'))


def search_place(place):
    "Search for place, return constituencies with that name"
    foundplace = geo.constituency(place)
    if foundplace:
        return Constituency.objects.filter(name__in=foundplace)
    else:
        return []

def search_name(place):
    "constituencies that have place in their name"
    return Constituency.objects\
        .filter(name__icontains=place)\
        .order_by('name')

def feedback(msg, place):
    "search feedback"
    return SafeUnicode(escape(msg) + (u"&nbsp;<b>%s</b>" % escape(place)))

def place_search(place):
    """
    Attempt to find the constituency for a place.

    Place can be a postcode, the name of a town, or the name of a constituency
    Returns a mapping that can be included in a context
    """
    results = []
    foundplace = search_place(place)
    if len(foundplace) > 0:
        if len(foundplace) == 1:
            fb = feedback("We found one constituency matching", place)
        else: 
            fb = feedback("We found these constituencies near", place)
        results.append((fb, foundplace))

    foundname = search_name(place)
    # some constituencies have exactly the same name as a town (eg
    # Nuneaton), they should not appear twice
    foundname = foundname.exclude(pk__in=foundplace)

    if len(foundname) > 0:
        fb = feedback("We found these constituencies containing", place)
        results.append((fb, foundname))
        
    if len(foundname) == 0 and len(foundplace) == 0:
        fb = feedback("Alas, we can't find", place)
        results.append((fb, []))

    return results


@login_required
def add_constituency(request):
    my_constituencies = request.user.current_constituencies.all()
    context = {'my_constituencies': my_constituencies}

    context['constituencies'] = []
    tick_instructions = "Tick a box and scroll"
    if len(my_constituencies) > 0:
        try:
            const = my_constituencies[0]
            neighbours = const.neighbors()
            for n in neighbours:
                if n in my_constituencies:
                    neighbours.remove(n)
            context["search_results"] = [
                (feedback("We found these constituencies near", const.name),
                 neighbours)]
        except KeyError:
            # Any problems looking up neighbours means we pretend to
            # have none
            pass

    # searching for a constituency by postcode or placename
    if request.method == "GET":
        if request.GET.has_key("q"):
            place = request.GET["q"]
            if not place.strip():
                context['search_results'] = (
                    "Please enter a postcode or place name", [])
            else:
                context["search_results"] = place_search(place)

    # adding another constituency
    if request.method == "POST":
        if request.POST.has_key('add') and request.POST.has_key('add_c'):
            add_c = request.POST.getlist('add_c')
            if type(add_c) != types.ListType:
                add_c = [add_c]
            constituencies = Constituency.objects.all().filter(slug__in=add_c)
            constituencies = constituencies.exclude(pk__in=my_constituencies)
            request.user.constituencies.add(*constituencies.all())
            request.user.save()
            return HttpResponseRedirect("/add_constituency/")

    return render_with_context(request,
                               'add_constituency.html',
                               context)

def do_login(request, key):
    profile = RegistrationProfile.objects.get_user(key)
    if profile:
        user = authenticate(username=profile.user.email)
        login(request, user)
    return HttpResponseRedirect("/")
    
def activate_user(request, key):
    profile = RegistrationProfile.objects.activate_user(key)
    error = notice = ""
    if not profile:
        error = "Sorry, that key was invalid"
    else:
        notice = "Thanks, you've successfully confirmed your email"
        user = authenticate(username=profile.user.email)
        login(request, user)
    context = {'error': error,
               'notice': notice}
    return HttpResponseRedirect(addToQueryString("/", context))

def user(request, id):
    context = {}
    user = get_object_or_404(CustomUser, pk=id)
    if user == request.user:
        context['user'] = user
    return render_with_context(request,
                               'user.html',
                               context)

def constituency(request, slug, year=None):
    if year:
        year = "%s-01-01" % year
    else:
        year = settings.CONSTITUENCY_YEAR
    try:
        constituency = Constituency.objects.all()\
                       .filter(slug=slug, year=year).get()
    except Constituency.DoesNotExist:
        raise Http404
    context = {'constituency': constituency}
    latspan = lonspan = 1
    missing = models.filter_where_customuser_fewer_than(1)
    missing_neighbours = constituency.neighbors(
        limit=5,
        constituency_set=missing)
    if missing_neighbours:
        furthest = missing_neighbours[-1]
        latspan = abs(furthest.lat - constituency.lat) * 2
        lonspan = abs(furthest.lon - constituency.lon) * 2
    context['latspan'] = latspan
    context['lonspan'] = lonspan
    return render_with_context(request,
                               'constituency.html',
                               context)

def constituencies_with_fewer_than_rss(request,
                                       volunteers=1):
    current_site = Site.objects.get_current()
    constituencies = models.filter_where_customuser_fewer_than(volunteers)
    context = {'constituencies': constituencies}
    context['site'] = current_site
    return render_to_response('geo.rss',
                              context,
                              context_instance=RequestContext(request),
                              mimetype="application/atom+xml")
    
def constituencies_with_more_than_rss(request,
                                       volunteers=1):
    current_site = Site.objects.get_current()
    constituencies = models.filter_where_customuser_more_than(volunteers)
    context = {'constituencies': constituencies}
    context['site'] = current_site
    return render_to_response('geo.rss',
                              context,
                              context_instance=RequestContext(request),
                              mimetype="application/atom+xml")

def statistics(request):
    context = {}
    context['histogram'] = models.date_joined_histogram()
    num_rows = context['histogram'].rowcount
    context['categorystep'] = int(num_rows / 40.0 * 4) + 1
    return render_with_context(request,
                               'statistics.html',
                               context)
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
