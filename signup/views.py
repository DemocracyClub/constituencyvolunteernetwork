import types
from itertools import takewhile
import re

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.utils.safestring import SafeUnicode
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

import models
from models import CustomUser, Constituency, RegistrationProfile
from forms import UserForm
import utils
import signals

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


def _get_statistics_context():
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
        percent = int(float(count)/total*100)
        context['percent_complete'] = percent
    else:
        context['percent_complete'] = 0
    return context

def home(request):
    context = _get_statistics_context()
    if request.user.is_anonymous():
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
    else:
        return HttpResponseRedirect(reverse('welcome'))

def home2(request):
    context = _get_statistics_context()
    if request.user.is_anonymous():
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
                               'home_2.html',
                               context)
    else:
        return HttpResponseRedirect(reverse('welcome'))

@login_required
def welcome(request):
    context = _get_statistics_context()        

    #context['usertasks'] = TaskUser.objects\
    #                           .filter(user=request.user)

    # "force" all new users to recruit for us
    if not request.user.seen_invite:
        return HttpResponseRedirect(reverse('inviteindex'))
    else:
        return render_with_context(request,
                                   'welcome.html',
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
    return SafeUnicode(escape(msg) + (u"&nbsp;<b>%s</b>:" % escape(place)))

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
    my_constituencies = request.user.ordered_constituencies.all()
    context = {'my_constituencies': my_constituencies}

    context['constituencies'] = []
    tick_instructions = "Tick a box and scroll"
    if len(my_constituencies) > 0:
        try:
            const = my_constituencies[0]
            all_const = Constituency.objects.exclude(
                pk__in=my_constituencies)
            neighbours = const.neighbors(limit=5,
                                         constituency_set=all_const)
            missing = models.filter_where_customuser_fewer_than(1)
            missing_neighbours = const.neighbors(
                limit=5,
                constituency_set=missing)

            context["search_results"] = [
                (feedback("We found these constituencies near", const.name),
                 neighbours)]
            context["missing_search_results"] = [
                (feedback(("These are the nearest places where there "
                           "aren't any volunteers yet"), ""),
                 missing_neighbours)]
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
        signals.user_login.send(None, user=user)
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
    context['profile_user'] = user
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
        
        if None not in (furthest.lat, furthest.lon,
                        constituency.lat, constituency.lon):
            # not in Northern Ireland
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

def generate_map(request):
    source_map = render_to_string('constituency-map.svg',{})
    year = settings.CONSTITUENCY_YEAR
    levels = {0:'level1',
              0.1:'level2',
              0.2:'level3',
              0.3:'level4',
              0.4:'level5',
              0.5:'level6',
              0.6:'level7',
              0.7:'level8',
              0.8:'level9',
              0.9:'level10'}
    level_keys = levels.keys()
    level_keys.sort()
    lines = []
    mapping = utils.map_id_to_const_name
    for line in source_map.splitlines():
        the_id = re.search('id="(seat-\d+)"', line)
        if the_id:
            level = 'none'
            the_name = mapping[the_id.group(1)]
            the_place = Constituency.objects\
                        .filter(year=year)\
                        .filter(name=the_name)
            if the_place:
                the_count = the_place[0]\
                            .customuser_set\
                            .filter(is_active=True)\
                            .count()
                score = min(float(the_count)/10, 1)
                for l in takewhile(lambda x: score > x, level_keys):
                    level = levels[l]
            line = line.replace('class="', 'class="%s ' % level)
        lines.append(line)
    return HttpResponse("\n".join(lines), mimetype="image/svg+xml")

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")

