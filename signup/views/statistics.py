import re
from itertools import takewhile

from django.http import HttpResponseRedirect, Http404, HttpResponse
from django.contrib.sites.models import Site
from django.template.loader import render_to_string

import settings
import utils

from signup.views import render_with_context
from signup.models import Constituency
import signup.models as models

def constituencies_with_fewer_than_rss(request,
                                       volunteers=1):
    current_site = Site.objects.get_current()
    constituencies = models.filter_where_customuser_fewer_than(volunteers)
    context = {'constituencies': constituencies}
    context['site'] = current_site
    return render_with_context(request,
                              'geo.rss',
                              context,
                              mimetype="application/atom+xml")
    
def constituencies_with_more_than_rss(request,
                                       volunteers=1):
    current_site = Site.objects.get_current()
    constituencies = models.filter_where_customuser_more_than(volunteers)
    context = {'constituencies': constituencies}
    context['site'] = current_site
    return render_with_context(request,
                              'geo.rss',
                              context,
                              mimetype="application/atom+xml")

def statistics(request):
    context = {}
    context['histogram'] = models.date_joined_histogram()
    num_rows = context['histogram'].rowcount
    context['categorystep'] = int(num_rows / 40.0 * 4) + 1
    context['const_volunteers'] = \
      models.constituency_volunteers_histogram(Constituency.objects.all())
    
    return render_with_context(request,
                               'statistics.html',
                               context)

def generate_map(request, date=None):
    source_map = render_to_string('constituency-map.svg',{})
    year = settings.CONSTITUENCY_YEAR
    levels = {0:'level1',
              0.1:'level2',
              0.2:'level3',
              0.3:'level4',
              0.4:'level5',
              0.5:'level6',
              0.6:'level7',
              0.7:'level8',
              0.8:'level9',
              0.9:'level10'}
    level_keys = levels.keys()
    level_keys.sort()
    lines = []       

    mapping = utils.map_id_to_const_name
    for line in source_map.splitlines():
        the_id = re.search('id="(seat-\d+)"', line)
        if the_id:
            level = 'none'
            the_name = mapping[the_id.group(1)]
            the_place = Constituency.objects\
                        .filter(year=year)\
                        .filter(name=the_name)
            if the_place:
                the_count = the_place[0]\
                            .customuser_set\
                            .filter(is_active=True)
                if date:
                    the_count = the_count.filter(date_joined__lt=date)
                the_count = the_count.count()
                score = min(float(the_count)/10, 1)
                for l in takewhile(lambda x: score > x, level_keys):
                    level = levels[l]
            line = line.replace('class="', 'class="%s ' % level)
        lines.append(line)
    return HttpResponse("\n".join(lines), mimetype="image/svg+xml")

def generate_map_2010(request, date=None):
    from slugify import smart_slugify
    
    source_map = render_to_string('constituency-map-2010.svg',{})
    year = settings.CONSTITUENCY_YEAR
    levels = {0:'level1',
              0.1:'level2',
              0.2:'level3',
              0.3:'level4',
              0.4:'level5',
              0.5:'level6',
              0.6:'level7',
              0.7:'level8',
              0.8:'level9',
              0.9:'level10'}
    level_keys = levels.keys()
    level_keys.sort()
    lines = []
    r = re.compile(r" id=\"([^\"]+)\" ")
    
    for line in source_map.splitlines():
        result = r.search(line)

        if result:
            slug = smart_slugify(result.groups(1)[0].lower())

            constituency = None
            if slug == "orkney-shetland-box":
                pass
            else:
                try:
                    constituency = Constituency.objects.get(slug=slug,year=year)
                except Constituency.DoesNotExist:
                    slug = slug.replace("-and", "")
                    try:
                        constituency = Constituency.objects.get(slug=slug,year=year)
                    except Constituency.DoesNotExist:
                        pass
                
            if constituency:
                level = 'none'
                the_count = constituency.customuser_set.filter(is_active=True)

                if date:
                    the_count = the_count.filter(date_joined__lt=date)
                
                score = min(float(the_count.count())/10, 1)
                for l in takewhile(lambda x: score > x, level_keys):
                    level = levels[l]
                line = line.replace('class="', 'class="%s ' % level)
        lines.append(line)
    return HttpResponse("\n".join(lines), mimetype="image/svg+xml")
