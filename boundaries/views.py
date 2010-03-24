from PIL import Image, ImageDraw
from django.http import HttpResponse, Http404
from django.shortcuts import render_to_response
from boundaries.models import Boundary
from django.contrib.gis.geos import Polygon, Point
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

def tile(request, mapname, tz=None, tx=None, ty=None):
    options = maps[str(mapname)]
    west, south, east, north = getTileRect(tx, ty, tz)
    zoom = 2 ** float(tz)
    tx = float(tx)
    ty = float(ty)
    image = Image.new("RGBA", (256, 256), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    #rr = 10
    for boundary in Boundary.objects.filter(boundary__intersects=Polygon([(east, north),(west, north),(west, south),(east, south),(east, north)])):
        #draw.text((10, rr),boundary.constituency.name, "black")
        #rr = rr + 10
        polyggon_options = options["polygon_options"](boundary)
        for polygon in boundary.boundary.coords:
                l = []
                for lat, lng in polygon:
                    x = 256 * (lat - west) / (east - west)
                    y = 256 * (lng - north) / (south - north)
                    l.append((x, y))
                draw.polygon(l, **polyggon_options)
    del draw
    response = HttpResponse(mimetype="image/png")
    image.save(response, "PNG")
    return response

def popup(request, mapname, x=None, y=None):
    options = maps[str(mapname)]
    b = Boundary.objects.filter(boundary__contains=Point(float(x), float(y)))
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
