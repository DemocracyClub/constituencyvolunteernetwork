from PIL import Image, ImageDraw
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from boundaries.models import Boundary
# from django.contrib.gis.geos import Polygon, Point
import math
import random

maps = {"id": {"polygon_options": lambda boundary:{"fill": (boundary.constituency.id / 3,  
                                                            boundary.constituency.id / 6, 
                                                            boundary.constituency.id / 6, 
                                                            60),
                                                   "outline": "black"},
               "template": lambda boundary: "popup_id.html",
                       },
        "volunteers": {"polygon_options": lambda boundary:{"fill": (20 * boundary.constituency.customuser_set.count(), 
                                                                    5 * boundary.constituency.customuser_set.count(), 
                                                                    5 * boundary.constituency.customuser_set.count(), 
                                                                    20),
                                                           "outline": "black"},
                       "template": lambda boundary: "popup_volunteers.html",
                       }
        }

def getDBzoom(z):
    if int(z) > 10:
        return 10
    else:
        return int(z)

def get_within(dbz, viewport):
    return Boundary.objects.filter(zoom=5)

def contains_point(dbz, x, y):
    return Boundary.objects.filter(zoom=5)[0]

def parse_polygon(poly_string):
    poly_string = poly_string.replace(u'POLYGON ((', u'')
    poly_string = poly_string.replace(u'))', u'')
    points = poly_string.split(u",")
    
    poly_coords = []
    for point in points:
        coords = point.split()
        
        if len(coords) == 2:
            poly_coords.append((float(coords[0]), float(coords[1])))
    
    return poly_coords

def parse_polygons(polys_string):
    return [polys_string]

"POLYGON ((-191270.3444430000090506 7060970.6321040000766516, -201139.8683899999887217 7078288.7933710003271699, -220550.1566870000096969 7073259.3950990000739694, -224321.5654670000076294 7053705.0302200000733137, -223377.9022230000118725 7033390.6230990001931787, -207366.0382690000114962 7021074.8138929996639490, -202005.1803490000020247 7040062.0499020004644990, -185182.9440060000051744 7053874.2623749999329448, -191270.3444430000090506 7060970.6321040000766516))"

def tile(request, mapname, tz=None, tx=None, ty=None):
    options = maps[str(mapname)]
    west, south, east, north = getTileRect(tx, ty, tz)
    zoom = 2 ** float(tz)
    tx = float(tx)
    ty = float(ty)
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    dbz = getDBzoom(tz)
    
    viewport = [(east, north),(west, north),(west, south),(east, south),(east, north)]
    boundaries_within = get_within(dbz, viewport) # Boundary.objects.filter(zoom=int(dbz), boundary__intersects=viewport):
    for boundary in boundaries_within:
        polyggon_options = options["polygon_options"](boundary)

        coords = parse_polygons(boundary.boundary)
        
        for polygon in coords:
            poly_coords = parse_polygon(polygon)
            
            l = []
            for lat, lng in poly_coords:
                x = 256 * (lat - west) / (east - west)
                y = 256 * (lng - north) / (south - north)
                l.append((x, y))
            l = reduce_polygon(l)
            
            draw.polygon(l, **polyggon_options)
    del draw
    response = HttpResponse(mimetype="image/png")
    image.save(response, "PNG")
    return response

def reduce_polygon(l):
    r = l[:1]
    for p in l[1:-1]:
        if dist2(r[-1], p) > 1:
            r.append(p)
    r.append(l[-1])
    return r

def dist2(a, b):
    (ax, ay) = a
    (bx, by) = b
    return (ax - bx) ** 2 + (ay - by) ** 2

def popup(request, mapname, x=None, y=None, z=None):
    options = maps[str(mapname)]
    dbz = getDBzoom(z)
    b = contains_point(int(dbz), x, y)# Boundary.objects.filter(zoom=int(dbz), boundary__contains=Point(float(x), float(y)))
    if len(b) == 0:
        raise Http404
    return render_to_response(options["template"](b[0]), {'constituency': b[0].constituency})


dist = 20037508.34
def to_googleX(x, tilesAtThisZoom):
  return -20037508.34 * (1 - 2 * float(x) / tilesAtThisZoom)

def to_googleY(x, tilesAtThisZoom):
  return 20037508.34 * (1 - 2 * float(x) / tilesAtThisZoom)

def getTileRect(xt, yt, zoomt):
           zoom = int(zoomt)
           x = int(xt)
           y = int(yt)
           tilesAtThisZoom = 2 ** zoom

           return (to_googleX(x, tilesAtThisZoom), 
                   to_googleY(y + 1, tilesAtThisZoom), 
                   to_googleX(x + 1, tilesAtThisZoom), 
                   to_googleY(y, tilesAtThisZoom))
