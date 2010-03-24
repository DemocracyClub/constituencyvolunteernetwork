from django.contrib.gis.db import models
from signup.models import Constituency

class Boundary(models.Model):
    constituency = models.ForeignKey(Constituency)
    boundary = models.PolygonField(srid=900913)
    objects = models.GeoManager()

#To find what constituencies where clicked on
#qs = Boundary.objects.filter(boundary__poly__contains='POINT(-104.590948 38.319914)')

#To find what constituencies need rendering in a particular tile
#tileGeom = GEOSGeometry('POLYGON (( 10 10, 10 20, 20 20, 20 15, 10 10))')
#qs = Boundary.objects.filter(poly__bboverlaps=tileGeom)
