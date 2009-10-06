import types
import time

from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.contrib.flatpages.models import FlatPage
from django.contrib.auth.decorators import login_required

from models import CustomUser, Constituency, RegistrationProfile
from forms import UserForm
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

def home(request):
    context = {}
    year = settings.CONSTITUENCY_YEAR
    constituencies = Constituency.objects.filter(year=year)
    count = CustomUser.objects\
            .aggregate(Count('constituencies',
                             distinct=True)).values()[0]
    total = constituencies.count()
    
    context['volunteers'] = CustomUser.objects.count()
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

@login_required
def add_constituency(request):
    my_constituencies = request.user.current_constituencies.all()
    context = {'my_constituencies': my_constituencies}

    context['constituencies'] = []
    tick_instructions = "Tick a box and scroll"
    if len(my_constituencies) > 0:
        try:
            const = my_constituencies[0]
            neighbours = Constituency.neighbours(const)
            neighbours = neighbours.exclude(pk__in=my_constituencies)
            context["search_term"] = const.name
            context['search_feedback'] = "We found these constituencies near"
            context['constituencies'] = neighbours
        except KeyError:
            # Any problems looking up neighbours means we pretend to
            # have none
            pass

    # searching for a constituency by postcode or placename
    if request.method == "GET":
        if request.GET.has_key("q"):
            place = request.GET["q"]
            if not place.strip():
                context['search_feedback'] = "Please enter a postcode or place name"
            else:
                foundplace = geo.constituency(place)            
                constituencies = []
                if foundplace:
                    constituencies = Constituency.objects.filter(name__in=foundplace)
                    if len(constituencies) == 1:
                        feedback = "We found one constituency matching"
                    else: 
                        feedback = "We found these constituencies near"


                if len(constituencies) == 0:
                    # if this gets results, the query has words that are
                    # contained in the names of constituencies. The order
                    # of the records coming out of the db is undefined, so
                    # alpha by name is reasonable
                    constituencies = Constituency.objects\
                                     .filter(name__icontains=place)\
                                     .order_by('name')
                    if len(constituencies) > 0:
                        feedback = "We found these constituencies containing"
                    else:
                        feedback = "Alas, we can't find"
                context["search_term"] = place
                context['constituencies'] = constituencies
                context['search_feedback'] = feedback

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
    context = {'constituency':constituency}
    return render_with_context(request,
                               'constituency.html',
                               context)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
