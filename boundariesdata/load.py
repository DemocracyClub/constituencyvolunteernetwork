from xml.dom.minidom import parse, parseString
from signup.models import Constituency
from boundaries.models import Boundary
from django.contrib.gis.geos import Point
maxZoom = 10

google_dist = 20037508.34

for f in ['boundariesdata/england.kml', 
          'boundariesdata/wales.kml', 
          'boundariesdata/scotland.kml', 
          'boundariesdata/northern_ireland.kml']:
    print f
    places = parse(f).getElementsByTagName("Placemark")
    for place in places:
        name = place.getElementsByTagName("name")[0].childNodes[0].toxml()
        print name
        v = []
        for coords in place.getElementsByTagName("coordinates"):
            points = []
            north = - google_dist
            south = google_dist
            east = - google_dist
            west = google_dist
            for coord in coords.childNodes[0].toxml().split(" "):
                s = coord.split(",")
                if len(s) == 3:
                    x, y = [float(c) for c in coord.split(",")][:2]
                    p = Point(x, y, srid=4326)
                    p.transform(900913)
                    gx, gy = p.coords
                    if gy > north: north = gy
                    if gy < south: south = gy                    
                    if gx > east: east = gx
                    if gx < west: west = gx
                    points.append((gx, gy))
            print "points", len(points)
            for z in range(maxZoom + 1):
                pixelsize2 = ((2 * google_dist / 256) / (2 ** z)) ** 2
                u = []
                previousX = 1e20
                previousY = 1e20
                for x, y in points:
                    if z == maxZoom:
                        u.append("(%f, %f)" % (x, y))
                    elif (x - previousX) ** 2 + (y - previousY) ** 2 > pixelsize2:
                        u.append("(%f, %f)" % (x, y))
                        previousX, previousY = x, y
                if z != maxZoom and (previousX, previousY) != (x, y):
                    u.append("(%f, %f)" % (x, y))
                print len(u)
                if len(u) > 3:
                    constituency = Constituency.objects.get(name = name)
                    boundary="[%s]" % reduce(lambda x, y: "%s, %s" %(x, y), u).strip()
                    b=Boundary(zoom = z, 
                               constituency = constituency, 
                               boundary=boundary,
                               east = east,
                               west = west,
                               north = north,
                               south = south)
                    try:
                        b.save()
                    except: 
                        print boundary

        if len(v) >= 1:
            print "'%s'" % name
