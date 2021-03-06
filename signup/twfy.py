import urllib
import copy
import csv
import datetime
from utils import json

import settings

api_key = "FH8qJGE5t7opGVTuXTDumuUK"
service_url = "http://www.theyworkforyou.com/api/"

params = {'key': api_key,
          'output': 'js'}

URL_OF_2010_TSV = "http://www.theyworkforyou.com/boundaries/new-constituencies.tsv"

from django.core.cache import cache

class Fetcher(object):
    "Fetches urls and caches the result"
    def __call__(self, url):
        chit = cache.get(url)
        if chit:
            return chit
        else:
            try:
                resp = urllib.urlopen(url)
                cval = resp.headers, resp.read()
            except IOError:
                cval = None, None
            cache.set(url, cval)
            return cval
            
    def prime(self, url, cval):
        cache.set(url, cval)

fetch = Fetcher()


def charset(headers):
    "charset of content"
    ctype = headers['content-type']
    return ctype[ctype.find("charset=")+len("charset="):]

def svcurl(method, sparams):
    """
    Return the twfy api url for a method
    """
    p = params.copy()
    p.update(sparams)
    return service_url + method + "?" + urllib.urlencode(p)




def getConstituency(postcode):
    "Constituency postcode is in"
    params = {"postcode": postcode}
    if settings.CONSTITUENCY_YEAR.strftime("%Y") >= "2010":
        # XXX this is temporary hack until elegant TWFY API solution
        # happens 
        params['future'] = 1
    _, response = fetch(svcurl("getConstituency", params))
    result = json.loads(response)
    if not result.has_key('error'):
        return result['name']
    else:
        return None


def getConstituencies(**kw):
    """
    A list of constituencies

    args - either:
      date - the list of constituencies as it was on this date

    or:
      latitude, longitude, distance - list of constituencies
                                 within distance of lat, lng
    """
    geoargs = ("latitude", "longitude", "distance")
    validargs = ("date", ) + geoargs

    invalid_args = list(k for k in kw.keys() if k not in validargs)
    if len(invalid_args) > 0:
        raise ValueError("Invalid args %r" % ",".join(invalid_args))

    if any(kw.has_key(k) for k in geoargs):
        if not all(kw.has_key(k) for k in geoargs):
            raise ValueError("Need all geoargs")

    params = dict((k, v) for k,v in kw.items() if v != None)
    new_constituency_date = "2010"
    date = kw.get('date', '2009')
    if date < new_constituency_date:
        headers, result = fetch(svcurl("getConstituencies", params))
        return json.loads(result, encoding=charset(headers))
    else:
        # XXX hopefully there will be a proper API for this in the future
        tsv_data = csv.DictReader(urllib.urlopen(URL_OF_2010_TSV),
                                  dialect='excel-tab')
        return tsv_data

def getGeometry(name=None):
    """
    Centre and bounding box of constituencies

    Don't provide any argument to get all constituencies
    """
    if name:
        params = dict(name=name)
    else:
        params = dict()
    if settings.CONSTITUENCY_YEAR.strftime("%Y") >= "2010":
        # XXX this is temporary hack until elegant TWFY API solution
        # happens 
        params['future'] = 1
    headers, result = fetch(svcurl("getGeometry", params))
    if name:
        data = json.loads(result, encoding=charset(headers))
    else:
        data = json.loads(result, encoding=charset(headers))["data"]
    return data

def getCurrentMP(name):
    """Return the current MP data structure for the named constituency
    
    """
    params = dict(constituency=name)
    headers, result = fetch(svcurl("getMP", params))
    try:
        data = json.loads(result, encoding=charset(headers))
    except ValueError:
        data = "Unknown (server error)"
    return data
