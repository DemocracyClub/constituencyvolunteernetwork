import sys
import simplejson as json
from optparse import make_option
import urllib
import csv
from twfy.models import SurveyResponse
from twfy.models import Statement
from ynmp.models import Candidacy

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


from settings import TWFY_SECRET_KEY

class Command(BaseCommand):
    option_list =  BaseCommand.option_list + (
        make_option('--file', '-f', dest='filename',
                    action="store",
                    help="JSON file to load from"),
        make_option('--url', '-u', dest='url',
                    action="store",
                    help="JSON url to load from"),
        )
    help = "Load data from TWFY to local database"
                        
    def handle(self, *args, **options):
        filename = options.get('filename', None)
        url = options.get('url', None)
        if filename:
            data = csv.DictReader(open(filename, "r"))
        elif url:
            url += "?secret=" + TWFY_SECRET_KEY
            resp = urllib.urlopen(url)
            _, fileobj = resp.headers, resp
            data = csv.DictReader(fileobj)
            
        else:
            raise CommandError("Must specify one of url or file")
        
        for result in data:
            statement, created = Statement.objects.get_or_create(
                twfy_key=result['refined_issue_key_name'])
            national = result['national'] == "True"
            if created:
                statement.question = result['question']
                statement.national = national
                statement.save()
            if "--" in result['candidacy_key_name']:
                continue
            seat_id, candidate_id = result['candidacy_key_name'].split("-")
            try:
                candidacy = Candidacy.objects.get(
                    candidate__ynmp_id=candidate_id,
                    ynmp_constituency__ynmp_seat_id=seat_id)
            except Candidacy.DoesNotExist:
                print "skipping", candidate_id, seat_id
                continue
            response = SurveyResponse.objects.get_or_create(
                candidacy=candidacy,
                statement=statement,
                national=national,
                agreement=result['agreement'],
                more_explanation=result['more_explanation'])
            
