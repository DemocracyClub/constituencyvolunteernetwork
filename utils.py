from urlparse import urlparse
from cgi import parse_qs
import urllib

try:
    import json
except ImportError:
    import simplejson as json

import re
POSTCODE_RE = re.compile(r'\b[A-PR-UWYZ][A-HK-Y0-9][A-HJKSTUW0-9]?[ABEHMNPRVWXY0-9]? {0,2}[0-9][ABD-HJLN-UW-Z]{2}\b',re.I)



def addToQueryString(orig, extra_data):
    scheme, netloc, path, params, query, fragment = urlparse(orig)
    query_data = parse_qs(query)
    for k, v in extra_data.items():
        if not v:
            del(extra_data[k])
    query_data.update(extra_data)
    query = urllib.urlencode(query_data, True)
    base_url = ""
    if scheme and netloc:
        base_url += "%s://%s" % (scheme, netloc)
    if path:
        base_url += "%s" % path
    if params:
        base_url += ";%s" % params
    if query:
        base_url += "?%s" % query
    if fragment:
        base_url += "#%s" % fragment
    return base_url
