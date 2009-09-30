import sys, os

import heapq
from difflib import SequenceMatcher

from HTMLParser import HTMLParser
from itertools import cycle

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from django.db import transaction

from election.models import Candidate, Constituency, Party

class Command(BaseCommand):
    """
    Import Candidate details
    """
    @transaction.commit_on_success
    def handle(self, *args, **options):
        basedir = os.path.dirname(sys.argv[0])
        collfile = os.path.join(
            basedir, "election", "management", "commands", "candidatecollection.htm")

        parser = CandidateHTMLParser()
        parser.feed(open(collfile).read())

        succ = 0
        missing_constituencies = set()
        for idx, rec in enumerate(parser.rows):
            try:
                constituency = Constituency.objects.get(
                    name=guess_const(rec["constituency"]))
                party, _ = Party.objects.get_or_create(
                    name=canoc(rec["party"]))
                candidate = Candidate(name=rec["candidate"],
                                      email=rec["email"],
                                      constituency=constituency,
                                      party=party)
                candidate.save()
                succ += 1
            except Constituency.DoesNotExist:
                missing_constituencies.add(rec["constituency"])
        print "*" * 80
        print "Done, %i of %i records imported (from %s)" % (succ, idx, collfile)
        print "%i constituencies mentioned in import file but not found in DB:" % len(missing_constituencies)
        print "\n".join(sorted(missing_constituencies))


def canoc(name):
    "canonical constituency name"
    return name.replace(" and ", " & ")

possibilities = list(c.name for c in Constituency.objects.all())
pcache = {}
def guess_const(name):
    "guess constituency name"
    cname = canoc(name)
    if cname in possibilities:
        return cname
    if cname in pcache:
        # prevents the same constituency being printed many times
        return pcache[cname]
    # Meon Valley == Don Valley|0.86, that's clearly wrong - this
    # cutoff gives the fewest false positivies.
    guesses = close_matches(cname, possibilities, cutoff=0.87)
    if len(guesses) > 0:
        ratio, guess = guesses[0]
        print "Guessing %30s ==  %30s|%4.2f" % (name, guess, ratio)
        pcache[cname] = guess
        return guess
    else:
        # unknown - let the caller deal with the resulting error
        return cname
    
def close_matches(word, possibilities, n=3, cutoff=0.6):
    # copied from difflib and hacked to return ratios
    result = []
    s = SequenceMatcher()
    s.set_seq2(word)
    for x in possibilities:
        s.set_seq1(x)
        if s.real_quick_ratio() >= cutoff and \
           s.quick_ratio() >= cutoff and \
           s.ratio() >= cutoff:
            result.append((s.ratio(), x))

    # Move the best scorers to head of list
    return heapq.nlargest(n, result)



# Very quick and dirty parser for Julian Todd's candidatecollection
# file. Hopefully better interfaces all round in the near future
class CandidateHTMLParser(HTMLParser):
    def reset(self):
        HTMLParser.reset(self)
        self.fieldnames = "constituency party candidate email web".split()
        self.nextfield = cycle(self.fieldnames).next
        self.rows = []
        self.cols = None
        self.cfield = None

    def handle_starttag(self, tag, attrs):
        if tag == "tr":
            self.cols = dict.fromkeys(self.fieldnames, '')
        if tag == "td":
            self.cfield = self.nextfield()
        if tag == "a":
            if self.cfield == "candidate":
                self.cols["candidate-url"] = dict(attrs)["href"]

    def handle_data(self, data):
        if self.cols != None and self.cfield != None:
            self.cols[self.cfield] = data.strip()

    def handle_endtag(self, tag):
        if tag == "tr":
            if hasattr(self, "last"):
                if self.cols["constituency"].strip() == "":
                    self.cols["constituency"] = self.last["constituency"]
            if self.cols["candidate"] != None:
                self.rows.append(self.cols)
            self.last = self.cols
            self.cols = None

        

        
