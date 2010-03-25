from PIL import Image, ImageDraw
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from django.db.models import Q
from boundaries.models import Boundary
import math
import random
google_dist = 20037508.34

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

def tile(request, mapname, tz=None, tx=None, ty=None):
    options = maps[str(mapname)]
    west, south, east, north = getTileRect(tx, ty, tz)
    zoom = 2 ** float(tz)
    tx = float(tx)
    ty = float(ty)
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    dbz = getDBzoom(tz)
    boundaries_within = Boundary.objects.filter(zoom=dbz, south__lt=north, north__gt=south, east__gt=west, west__lt=east)
    for boundary in boundaries_within:
        polyggon_options = options["polygon_options"](boundary)
        coords = eval(boundary.boundary)
        l = []
        for lat, lng in coords:
            x = 256 * (lat - west) / (east - west)
            y = 256 * (lng - north) / (south - north)
            l.append((x, y))
        draw.polygon(l, **polyggon_options)
    del draw
    response = HttpResponse(mimetype="image/png")
    image.save(response, "PNG")
    return response

def popup(request, mapname, x=None, y=None, z=None):
    options = maps[str(mapname)]
    x = float(x)
    y = float(y)
    dbz = getDBzoom(z)
    possible_boundaries = Boundary.objects.filter(zoom=int(dbz), south__lt=y, north__gt=y, east__gt=x, west__lt=x)
    for boundary in possible_boundaries:
        coords = eval(boundary.boundary)
        inside = False
        for (vx0, vy0), (vx1, vy1) in zip(coords, coords[1:] + coords[:1]):
            if ((vy0>y) != (vy1>y)) and (x < (vx1-vx0) * (y-vy0) / (vy1-vy0) + vx0):
                inside = not(inside)
        if inside:
            return render_to_response(options["template"](boundary), {'constituency': boundary.constituency})
    raise Http404

def to_google(x, tilesAtThisZoom):
  return google_dist * (1 - 2 * float(x) / tilesAtThisZoom)

def getTileRect(xt, yt, zoomt):
           zoom = int(zoomt)
           x = int(xt)
           y = int(yt)
           tilesAtThisZoom = 2 ** zoom

           return (-to_google(x, tilesAtThisZoom), 
                   to_google(y + 1, tilesAtThisZoom), 
                   -to_google(x + 1, tilesAtThisZoom), 
                   to_google(y, tilesAtThisZoom))
