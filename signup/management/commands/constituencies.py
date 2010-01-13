import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction

from slugify import smart_slugify
from signup import models, twfy, geo
from settings import CONSTITUENCY_YEAR

class Command(BaseCommand):
    def handle(self, *args, **options):
        if not args or (args and args[0] not in ('load', 'update')):
            raise CommandError("USAGE: ./manage.py %s load" % \
                    os.path.basename(__file__).split('.')[0])

        transaction.enter_transaction_management()
        transaction.managed(True)

        year = CONSTITUENCY_YEAR.strftime("%Y")
        
        constituencies = twfy.getConstituencies(date=year)
        if args[0] == 'load':
            for c in constituencies:
                try:
                    lat, lon = (c['centre_lat'], c['centre_lon'])
                except KeyError:
                    # this happens for Northern Ireland - no geodata available
                    lat, lon = (None, None)

                # XXX new "api" inconsistuency
                name = c.get('name', c.get('Name', '')) 
                item = models.Constituency(name=name,
                                           year=CONSTITUENCY_YEAR,
                                           lat=lat,
                                           lon=lon)
                item.slug = smart_slugify(item.name, 
                                          manager=models.Constituency.objects,
                                          lower_case=True)

                if not ("silent" in options) or options["silent"] == False:
                    print "Loading %s <%s>" % (item.name, item.slug)

                item.save()
        else:
            geometries = twfy.getGeometry()
            for c in constituencies:
                name = c.get('name', c.get('Name', ''))
                item = models.Constituency.objects.\
                       filter(name=name,
                              year=CONSTITUENCY_YEAR).get()
                c.update(geometries[name])
                try:
                    item.lat = c['centre_lat']
                    item.lon = c['centre_lon']
                except KeyError:
                    # this happens for Northern Ireland
                    continue
                #if not ("silent" in options) or options["silent"] == False:
                #    print "Updating %s (%d, %d)" % \
                #          (item.name, item.lat, item.lon)
                item.save()
            for user in models.CustomUser.objects.all():
                constituency_name = twfy.getConstituency(user.postcode)
                try:
                    constituency = models.Constituency.objects.all()\
                                   .filter(name=constituency_name)\
                                   .filter(year=CONSTITUENCY_YEAR).get()
                except models.Constituency.DoesNotExist:
                    print "error:", user
                    continue
                user.constituencies.add(constituency)
                user.save()
                prior = user.constituencies.filter(year__lt=CONSTITUENCY_YEAR)
                prior = prior.order_by('signup_customuser_constituencies.id')
                if len(prior) > 1:
                    print user, "has extra constituencies"
                for extra in prior[1:]:

                    constituency_set = models.Constituency.objects\
                                       .filter(year=CONSTITUENCY_YEAR)
                    distances = []
                    for c in constituency_set:
                        if not c.lat or not extra.lat:
                            continue
                        distance = geo.haversine((c.lat, c.lon),
                                                 (extra.lat, extra.lon))

                        distances.append((c, distance))
                    nearest = sorted(distances, key=lambda x: x[1])
                    if nearest:
                        constituency = nearest[0][0]
                        print " old", extra, "new", constituency
                        user.constituencies.add(constituency)
                        user.save()
                    else:
                        print " couldn't work out new additionals for",user, extra
                #if not ("silent" in options) or options["silent"] == False:
                #    print "reset home constituency for %s" % user

                
        transaction.commit()
