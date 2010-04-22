import simplejson as json
from optparse import make_option
import urllib
import gzip

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError

from signup.models import Constituency
from ynmp.models import Party
from ynmp.models import Candidate
from ynmp.models import Candidacy
from ynmp.models import YNMPConstituency

class Command(BaseCommand):
    option_list =  BaseCommand.option_list + (
        make_option('--file', '-f', dest='filename',
                    action="store",
                    help="JSON file to load from"),
        make_option('--url', '-u', dest='url',
                    action="store",
                    help="JSON url to load from"),
        )
    help = "Load data from YNMP to local database"
                        
    def handle(self, *args, **options):
        filename = options.get('filename', None)
        url = options.get('url', None)
        if filename:
            data = open(filename, "r").read()
        elif url:
            resp = urllib.urlopen(url)
            _, data = resp.headers, resp.read()
            f = open("/tmp/data", "w")
            f.write(data)
            f.close()
            data = gzip.open("/tmp/data", "rb").read()
        else:
            raise CommandError("Must specify one of url or file")
        try:
            parsed = json.loads(data)
        except ValueError:
            print "Problem parsing", data
        for id, party in parsed['Party'].items():
            p, _ = Party.objects.get_or_create(name=party['name'],
                                                   ynmp_id=id)
            p.image_id = party['image_id']
            p.save()
            
        candidates = parsed['Candidate'].items()
        for id, candidate in candidates:
            item, _ = Candidate.objects.get_or_create(ynmp_id=id)
            item.status = candidate['status']
            item.email = candidate['email']
            item.updated = candidate['updated']
            item.gender = candidate['gender']
            item.code = candidate['code']
            item.university = candidate['university']
            item.name = candidate['name']
            item.phone = candidate['phone']
            item.dob = candidate['dob']
            item.ynmp_party_id = candidate['party_id']
            party = Party.objects.get(ynmp_id=item.ynmp_party_id)
            item.party = party
            item.save()
        seats = parsed['Seat'].items()
        for id, seat in seats:
            name = seat['name']
            try:
                constituency = Constituency.objects.get(name=name)
            except Constituency.DoesNotExist:
                name = name.replace(" and ", " & ")
                name = name.replace(u" M\xf4n", " Mon")
                constituency = Constituency.objects.get(name=name)
            item, _ = YNMPConstituency.objects\
                      .get_or_create(ynmp_seat_id=id,
                                     constituency=constituency)
            item.nominations_entered = bool(seat['nominations_entered'])
            item.nomination_url = seat['nomination_url']
            item.save()
        
        for id, candidacy in parsed['Candidacy'].items():
            ynmp_constituency = YNMPConstituency\
                                .objects.get(ynmp_seat_id=candidacy['seat_id'])
            candidate = Candidate.objects.get(ynmp_id=candidacy['candidate_id'])
            try:
                item = Candidacy.objects.get(ynmp_id=id)
                item.ynmp_constituency = ynmp_constituency
                item.candidate = candidate
                item.save()
            except Candidacy.DoesNotExist:
                Candidacy.objects.create(ynmp_id=id,
                                         ynmp_constituency=ynmp_constituency,
                                         candidate=candidate)
        
