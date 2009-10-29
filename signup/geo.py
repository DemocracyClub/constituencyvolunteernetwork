import math
import twfy
import urllib

from utils import json, POSTCODE_RE

def haversine((lat1, lon1), (lat2, lon2)):
    """
    Haversine distance between two points
    """
    R = 6371; # Earth's radius in km
    dLat = math.radians(lat2-lat1)
    dLon = math.radians(lon2-lon1)
    a = (math.sin(dLat/2) * math.sin(dLat/2) + math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) * math.sin(dLon/2) * math.sin(dLon/2) )
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a)); 
    return R * c


# nicked from http://github.com/simonw/geocoders/
def geocode(q):
    data = json.load(urllib.urlopen(
        'http://ws.geonames.org/searchJSON?' + urllib.urlencode({
            'q': q,
            'maxRows': 1,
            'lang': 'en',
            'style': 'full',
            'country': 'GB'
        })
    ))
    if not data['geonames']:
        return None, (None, None)
    
    place = data['geonames'][0]
    name = place['name']
    if place['adminName1'] and place['name'] != place['adminName1']:
        name += ', ' + place['adminName1']
    return name, (place['lat'], place['lng'])


def constituency(place):
    try:
        if POSTCODE_RE.match(place):
            const = twfy.getConstituency(place)
            if const == None:
                return None
            else:
                return [const]
        else:
            _, (lat, lng) = geocode(place)
            
            consts = None
            distance = 10
            while not consts:
                # Only likely to actually loop in extreme, circumstances,
                # e.g. "Haltwhistle". See issue 19
                consts = twfy.getConstituencies(latitude=lat,
                                                longitude=lng,
                                                distance=distance)
                distance = distance * 2
            
            return [x['name'] for x in consts]
    except Exception:
        return None
    
