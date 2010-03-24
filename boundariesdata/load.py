from xml.dom.minidom import parse, parseString
from signup.models import Constituency
from boundaries.models import Boundary

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
            u = []
            for coord in coords.childNodes[0].toxml().split(" "):
                s = coord.split(",")
                if len(s) == 3:
                    u.append("%s %s" % tuple([c for c in coord.split(",")][:2]))
            if len(u) > 1:
                constituency = Constituency.objects.get(name = name)
                boundary="SRID=4326;POLYGON((%s))" % reduce(lambda x, y: "%s, %s" %(x, y), u).strip()
                b=Boundary(constituency = constituency, boundary=boundary)
                try:
                    b.save()
                except: 
                    print boundary

        if len(v) >= 1:
            print "'%s'" % name
