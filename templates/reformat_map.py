import os, sys
from os.path import dirname
import re

if 'DJANGO_SETTINGS_MODULE' not in os.environ:
    sys.path.insert(0, (dirname(__file__) or '.') + '/..') # put settings.py on path
    os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

from signup.models import Constituency
from settings import CONSTITUENCY_YEAR
from slugify import smart_slugify

constituency_map = open("constituency-map-2010-nl.svg", "r").read()
constituency_map = constituency_map.replace("><path", ">\n<path")
constituency_map = constituency_map.replace("</g><g", "</g>\n<g")

f = open("constituency-map-2010-nl.svg", "w+")
f.write(constituency_map)
f.close()

