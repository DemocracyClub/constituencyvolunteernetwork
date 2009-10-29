import os

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction

from slugify import smart_slugify
from signup import models, twfy
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
                item = models.Constituency(name=c['name'],
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
                c.update(geometries[c['name']])
                item = models.Constituency.objects.\
                       filter(name=c['name']).get()
                try:
                    item.lat = c['centre_lat']
                    item.lon = c['centre_lon']
                except KeyError:
                    # this happens for Northern Ireland
                    continue
                if not ("silent" in options) or options["silent"] == False:
                    print "Updating %s (%d, %d)" % \
                          (item.name, item.lat, item.lon)
                item.save()
                
        transaction.commit()
