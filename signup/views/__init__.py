import types

from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.html import escape
from django.utils.safestring import SafeUnicode
from django.contrib.sites.models import Site
from django.template.loader import render_to_string
from django.core.mail import send_mail

from signup.util import render_with_context
import settings

import signup.models as models
from signup.models import CustomUser, Constituency, RegistrationProfile
from signup.forms import UserForm
import signup.signals as signals
import signup.geo as geo

from tasks.util import login_key

from tasks.activity import generate_activity
from comments_custom.models import NotifyComment

def _get_statistics_context():
    context = {}
    year = settings.CONSTITUENCY_YEAR
    constituencies = Constituency.objects.filter(year=year)
    volunteers = CustomUser.objects.filter(is_active=True)
    count = constituencies.filter(customuser__in=volunteers)\
            .distinct()\
            .count()
    total = constituencies.count()
    
    context['volunteers'] = volunteers.count()
    context['total'] = total
    context['count'] = count
    if total:
        percent = int(float(count)/total*100)
        context['percent_complete'] = percent
    else:
        context['percent_complete'] = 0
    context['new_signups'] = CustomUser.objects.order_by('-date_joined')\
                                               .filter(can_cc=True)[:5]
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
def delete_constituency(request, slug):
    year = settings.CONSTITUENCY_YEAR
    c = Constituency.objects.get(slug=slug,
                                 year=year)
    request.user.constituencies.remove(c)
    request.user.save()

    signals.user_leave_constituency.send(None,
                                         user=request.user,
                                         constituencies=[c])
    
    return HttpResponseRedirect(reverse('add_constituency'))


def search_place(place):
    "Search for place, return constituencies with that name"
    foundplace = geo.constituency(place)
    if foundplace:
        return Constituency.objects.filter(name__in=foundplace,
                                           year=settings.CONSTITUENCY_YEAR)
    else:
        return []

def search_name(place):
    "constituencies that have place in their name"
    return Constituency.objects\
        .filter(name__icontains=place,
                year=settings.CONSTITUENCY_YEAR)\
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


def _get_nearby_context(request):
    """Returns a context suitable for displaying and searching lists of
    nearby constituencies
    """
    my_constituencies = []
    if hasattr(request.user, 'ordered_constituencies'):
        my_constituencies = request.user.ordered_constituencies.all()
    context = {'my_constituencies': my_constituencies}
    context['constituencies'] = []
    tick_instructions = "Tick a box and scroll"
    if len(my_constituencies) > 0:
        try:
            const = my_constituencies[0]
            year = settings.CONSTITUENCY_YEAR
            all_const = Constituency.objects.filter(year=year)
            all_const = all_const.exclude(pk__in=my_constituencies)
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
    return context
    
@login_required
def add_constituency(request):
    context = _get_nearby_context(request)
    # adding another constituency
    if request.method == "POST":
        if request.POST.has_key('add') and request.POST.has_key('add_c'):
            add_c = request.POST.getlist('add_c')
            if type(add_c) != types.ListType:
                add_c = [add_c]
            constituencies = Constituency.objects.all()\
                             .filter(slug__in=add_c)
            mine = context['my_constituencies']
            constituencies = constituencies.exclude(pk__in=mine)
            request.user.constituencies.add(*constituencies.all())
            request.user.save()
            sig = signals.user_join_constituency
            sig.send(None,
                     user=request.user)
            return HttpResponseRedirect("/add_constituency/")

    return render_with_context(request,
                               'add_constituency.html',
                               context)

def constituencies(request):
    year = settings.CONSTITUENCY_YEAR
    context = {}
    context['constituencies'] = Constituency.objects.all()\
                                .filter(year=year)\
                                .order_by('name')
    return render_with_context(request,
                               'constituencies.html',
                               context)

@login_key
def constituency(request, slug, year=None):
    context = _get_nearby_context(request)

    if year:
        year = "%s-01-01" % year
    else:
        year = settings.CONSTITUENCY_YEAR

    try:
        constituency = Constituency.objects.all()\
                       .filter(slug=slug, year=year).get()
        context['constituency'] = constituency
    except Constituency.DoesNotExist:
        raise Http404
    
    if request.method == "POST" and 'notifypost' in request.POST:
        try:
            notify_object = NotifyComment.objects.get(user=request.user,
                                                      constituency=constituency)
        except NotifyComment.DoesNotExist:
            notify_object = NotifyComment.objects.create(user=request.user,
                                                         constituency=constituency,
                                                         notify_type=NotifyComment.Types.none)

        if 'notify' in request.POST:
            notify_object.notify_type = NotifyComment.Types.every
        else:
            notify_object.notify_type = NotifyComment.Types.none

        notify_object.save()

        return HttpResponseRedirect(reverse('constituency', args=[slug]))
    
    elif request.method == "POST" and 'subject' in request.POST:
        within_km = int(request.POST['within_km'])
        nearest = constituency.neighbors(limit=100,
                                         within_km=within_km)
        nearest = nearest + [constituency]
        context['nearest'] = nearest
        context['subject'] = request.POST['subject']
        context['message'] = request.POST['message']
        context['within_km'] = within_km
        couldnt_send = []
        if request.POST.get('go', ''):
            count = 0
            site = Site.objects.get_current()
            for c in nearest:
                for user in c.customuser_set.filter(is_active=True):
                    try:
                        profile = user.registrationprofile_set.get()
                        footer = render_to_string('email_unsub_footer.txt',
                                                  {'site':site,
                                                   'user_profile':profile})
                        message = "%s\n\n%s" % (request.POST['message'],
                                                footer)
                        send_mail(request.POST['subject'],
                                  message,
                                  settings.DEFAULT_FROM_EMAIL,
                                  [user.email,])
                        count += 1
                    except RegistrationProfile.DoesNotExist:
                        couldnt_send.append(user)
            context['recipients'] = count
            context['error_recipients'] = couldnt_send
        return render_with_context(request,
                                   'constituency_email.html',
                                   context)
    else:
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
        context['activity'] = generate_activity([constituency], show_constituency=False)
  
        if request.user.is_authenticated():
            context['volunteer_here'] = bool(request.user.constituencies.filter(id=constituency.id))
        else:
            context['volunteer_here'] = False

        context['is_constituency_page'] = True
    
        try:
            context['notify_object'] = NotifyComment.objects.get(user=request.user,
                                                          constituency=constituency)
        except NotifyComment.DoesNotExist:
            context['notify_object'] = None
        
        return render_with_context(request,
                                   'constituency.html',
                                   context)

