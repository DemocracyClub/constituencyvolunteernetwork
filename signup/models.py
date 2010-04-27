# python
import datetime
import random
import re
import hashlib
from itertools import chain
# django
from django.db import models
from django.db.models import Model as DjangoModel
from django.db.models import permalink
from django.db.models import Count
from django.contrib.auth.models import User, UserManager
from django.conf import settings
from django.template.loader import render_to_string
from django.contrib.sites.models import Site
from django.core.mail import send_mail

# app
import geo
from slugify import smart_slugify
from settings import CONSTITUENCY_YEAR
import signals
import twfy
import wiki_constituencies
import tsc_constituencies
import hashtags

SHA1_RE = re.compile('^[a-f0-9]{40}$')

class Model(DjangoModel):
    class Meta:
        abstract = True
    """same as django model but allows you to be lazy about the slug"""
    def __init__(self, *args, **kwargs):
        if not kwargs.get('slug') and 'slug' in self._meta.get_all_field_names():
            if kwargs.get('title'):
                kwargs['slug'] = smart_slugify(kwargs['title'], lower_case=True)
            elif kwargs.get('name'):
                kwargs['slug'] = smart_slugify(kwargs['name'], lower_case=True)
            elif kwargs:
                import warnings
                warnings.warn("Unable to automagically set slug (%s)" % \
                              self._meta.get_all_field_names())
        super(Model, self).__init__(*args, **kwargs)

class ThisYearConstituencyManager(models.Manager):
    def get_query_set(self):
        return super(ThisYearConstituencyManager, self)\
               .get_query_set()\
               .filter(year=CONSTITUENCY_YEAR)

class Constituency(Model):
    name = models.CharField(max_length=80)
    slug = models.SlugField(max_length=80)
    lat = models.FloatField(verbose_name='latitude',
                            blank=True,
                            null=True)
    lon = models.FloatField(verbose_name='longitude',
                            blank=True,
                            null=True)
    year = models.DateField()
    objects = ThisYearConstituencyManager()
    
    def __unicode__(self):
        return "%s (%s)" % (self.name, self.year)

    def twfy_slug(self):
        """Return a slug in the format used by the TWFY questionnaire
        app.
        """
        return self.slug.replace("-", "_")

    @property
    def tsc_slug(self):
        try:
            return tsc_constituencies.tsc_slugs[self.slug]
        except KeyError:
            return ""

    def distance_from(self, other):
        if None in (self.lat, self.lon, other.lat, other.lon):
            # must be Northern Ireland
            if None in (other.lat, other.lon) \
                   and None in (self.lat, self.lon):
                # both in Northern Ireland. For now, pretend they're
                # all on top of each other
                distance = 0
            else:
                distance = 10000
        else:            
            distance = geo.haversine((self.lat, self.lon),
                                 (other.lat, other.lon))
        return distance
    
    def neighbors(self, limit=7, within_km=100, constituency_set=None):
        distances = []
        if constituency_set is None:
            constituency_set = Constituency.objects\
                               .filter(year=CONSTITUENCY_YEAR)
        for c in constituency_set:
            distances.append((c, self.distance_from(c)))
        nearest = sorted(distances, key=lambda x: x[1])
        neighbours = []
        count = 0
        for place, distance in nearest[1:]:
            if limit and count >= limit:
                break
            if within_km and distance > within_km:
                break
            neighbours.append(place)
            count += 1
        return neighbours

    def current_mp(self):
        return twfy.getCurrentMP(self.name)

    @property
    def wikipedia_url(self):
        try:
            return wiki_constituencies.constituency_wikipedia[self.slug]
        except KeyError:
            return "http://en.wikipedia.org/wiki/Special:Search/%s_(UK_Parliament_constituency)" % self.slug

    @property
    def twitter_hashtag(self):
        try:
            return hashtags.constituency_hashtags[self.slug]
        except KeyError:
            return "ge2010"

    @property
    def ynmp_url(self):
        return "http://www.yournextmp.com/seats/%s" % self.slug.replace('-','_')

    @permalink
    def get_absolute_url(self):
        return ("constituency", (self.slug,))

    class Meta:
        verbose_name_plural = "Constituencies"
        
class CustomUser(User):
    postcode = models.CharField(max_length=9)
    constituencies = models.ManyToManyField(Constituency)
    can_cc = models.BooleanField(default=False)
    login_count = models.IntegerField(default=0)
    seen_invite = models.BooleanField(default=False)
    unsubscribed = models.BooleanField(default=False)
    objects = UserManager()
    display_name = models.CharField(max_length=30, default="Someone")
    points = models.IntegerField(default=0)
    hassling = models.BooleanField(default=False)
    
    @property
    def current_constituencies(self):
        "Return constituencies matching current year"
        return self.constituencies.filter(year=CONSTITUENCY_YEAR)

    @property
    def ordered_constituencies(self):
        "Return constituencies in the order in which they were added"
        return self.current_constituencies\
               .order_by('signup_customuser_constituencies.id')

    @property
    def home_constituency(self):
        "Return the first constituency the user subscribed to"
        if len(self.ordered_constituencies) > 0:
            return self.ordered_constituencies[0]
        else:
            return {"name": "no constituency",} # hack
        
    #@property
    #def display_name(self):
    #    """ Name appropriate for public display """
    #    if self.can_cc:
    #        if self.first_name:
    #            name = self.first_name
    #        else:
    #            name = "Someone"
    #    else:
    #        name = "Someone"
    #    return name

    @property
    def private_name(self):
        """ Name appropriate for private viewing, e.g. emails """
        if self.first_name:
            name = self.first_name
        else:
            name = self.email
        return name

    @property
    def full_name(self):
        if self.first_name or self.last_name:
            name = "%s %s" % (self.first_name, self.last_name)
        else:
            name = self.email
        return name

    @property
    def safe_email(self):
        return self.email.replace("@", " at ")
    
    def __unicode__(self):
        return self.email
    
    @permalink
    def get_absolute_url(self):
        return ("user", (self.id,))



class RegistrationManager(models.Manager):
    """
    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.
    
    """
    def activate_user(self, profile):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.
        """
        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        #profile = self.get_user(activation_key,
        #                        only_activated=False)
        if profile and not profile.activated and \
               not profile.activation_key_expired() and \
               not profile.user.unsubscribed:
            user = profile.user
            user.is_active = True
            user.save()
            profile.activated = True
            profile.save()
            signals.user_activated.send(self, user=user)
            return True
        else:
            return False

    def deactivate_user(self, profile, user_request=False):
        if profile:
            user = profile.user
            user.is_active = False
            if user_request:
                user.unsubscribed = True
            user.save()
            profile.activated = False
            profile.save()
            signals.user_deactivated.send(self, user=user)
            return True
        else:
            return False

    def get_user(self, activation_key, only_activated=True):
        profile = None
        if SHA1_RE.search(activation_key):
            profile = RegistrationProfile.objects.all()\
                      .filter(activation_key=activation_key)
            if only_activated:
                profile = profile.filter(activated=True)
            if profile:
                profile = profile[0]
        return profile
        
    def create_profile(self,
                       user):
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]
        activation_key = hashlib.sha1(salt+user.username).hexdigest()
        profile = RegistrationProfile(user=user,
                                      activation_key=activation_key)
        profile.save()

        user.is_active = False
        user.save()

        profile.send_activation_email()        
        
        return profile
    

    def delete_expired_users(self):
        for profile in RegistrationProfile.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()
                    profile.delete()


class RegistrationProfile(Model):
    """
    A simple profile which stores an activation key for use in passwordless
    site interaction

    """
    user = models.ForeignKey(CustomUser,
                             verbose_name='user')
    email = models.CharField(max_length=80)
    activation_key = models.CharField(max_length=50)
    objects = RegistrationManager()
    activated = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = 'registration profile'
        verbose_name_plural = 'registration profiles'
    
    def __unicode__(self):
        return u"Registration information for %s" % self.user
    
    def activation_key_expired(self):
        expiration_date = datetime.timedelta(
            days=settings.ACCOUNT_ACTIVATION_DAYS)
        return not self.activated and \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())

    def resend_activation_email(self):
        current_site = Site.objects.get_current()
        subject = "Can you confirm your Democracy Club registration?"
        email_context = {'activation_key': self.activation_key,
                         'site': current_site,
                         'user': self.user}
        message = render_to_string('activation_email_resend.txt',
                                   email_context)
        
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.user.email,])
        return self.user.email

    def send_activation_email(self):
        current_site = Site.objects.get_current()
        subject = "Please confirm your registration"
        email_context = {'activation_key': self.activation_key,
                         'site': current_site,
                         'user': self.user}
        message = render_to_string('activation_email.txt',
                                   email_context)
        
        send_mail(subject,
                  message,
                  settings.DEFAULT_FROM_EMAIL,
                  [self.user.email,])

    # XXX This is used in the admin interface, but not yet in the template.
    @permalink
    def get_login_url(self):
        return ( "login", (), { "key" : self.activation_key } )

    activation_key_expired.boolean = True

def constituency_volunteers_histogram(constituencies):
    count = {}
    for constituency in constituencies:
        k = constituency.customuser_set.filter(is_active=True).count()
        if k in count:
            count[k] += 1
        else:
            count[k] = 1
    return count

###############
# Raw SQL queries

def date_joined_histogram(previous_days=90):
    from django.db import connection
    sql = ("SELECT to_char(auth_user.date_joined, 'DD Mon') AS shortdate, "
           "COUNT(*), DATE_TRUNC('day', auth_user.date_joined) AS date "
           "FROM auth_user WHERE is_active = True "
           "AND auth_user.date_joined > now() - interval '%s days' "
           "GROUP BY date, shortdate "
           "ORDER BY date;")
    cursor = connection.cursor()
    cursor.execute(sql, [previous_days])
    return cursor
    
def _select_by_signup_count(count, operator="lt"):
    active = CustomUser.objects.filter(is_active=True)
    cons = Constituency.objects\
           .filter(year=CONSTITUENCY_YEAR)\
           .filter(customuser__in=active)\
           .annotate(num_users=Count('customuser'))
    zero_cons = Constituency.objects\
                .filter(year=CONSTITUENCY_YEAR)
    if cons:
        zero_cons = zero_cons.exclude(pk__in=[x.id for x in cons])
    for z in zero_cons:
        z.num_users = 0
    if operator == "lt":
        cons = cons.filter(num_users__lt=count)
        cons = list(chain(zero_cons, cons))
    elif operator == "gt":
        cons = cons.filter(num_users__gt=count)
    return cons

def filter_where_customuser_fewer_than(count):
    return _select_by_signup_count(count, operator="lt")

def filter_where_customuser_more_than(count):
    return _select_by_signup_count(count, operator="gt")


