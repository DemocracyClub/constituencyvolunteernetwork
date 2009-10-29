from unittest import TestCase

from signup import geo

class TestGeoConstituency(TestCase):
    """
    geo.constituency tries to give you the constituency that a "place"
    is in. Place may be a postcode or the name of a town.
    """
    def assertIn(self, val, container, msg=None):
        if not msg:
            msg = "%r not in %r" % (val, container)
        self.assert_(val in container, msg)

    def test_geocode(self):
        name, (lat, lng) = geo.geocode("Newham")
        self.assertIn(u"Newham", name)

    def test_town1(self):
        """ You can search for a town """
        self.assertIn("Crewe & Nantwich", geo.constituency("Crewe"))

    def test_town2(self):
        self.assertIn("Falkirk", geo.constituency("Alloa"))

    def test_town3(self):
        self.assertIn("Shipley", geo.constituency("Ilkley"))

    def _test_town4(self): # SKIPPED
        """ XXX this is broken because the twfy api have no data about Belfast """
        self.assertIn("Belfast", geo.constituency("Forkhill"))

    def test_postcode1(self):
        """ Test poscode - Land's End """
        self.assertIn("St Ives", geo.constituency("TR19 7AA"))

    def test_postcode_nonexistant(self):
        """ There are no postcodes that start with D """
        self.assertEquals(None, geo.constituency("D7 7QX"))

    def test_postcode_forces(self):
        """ Postcodes run by the British forces post office . We can't
        do anything with these (they don't point towards a
        constituency) """
        self.assertEquals(None, geo.constituency("BFPO 801"))
        
    def test_haltwhistle(self):
        """ Test for issue 19, names geocoding to locations > 10 miles
        away from a constituency """
        self.assertIn("Hexham", geo.constituency("Haltwhistle"))
