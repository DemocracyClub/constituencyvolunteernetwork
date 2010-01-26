# python
import datetime
import cgi

# django
from django.conf import settings
from django.contrib.flatpages.models import FlatPage
from django.contrib.sites.models import Site

# app
from testbase import TestCase

from signup.models import Constituency, CustomUser
from signup.views import place_search

users = [{'email':'f@mailinator.com',
          'postcode':'G206BT',
          'can_cc':True,
          'first_name':'f',
          'last_name':'f',
          'username':'f@mailinator.com'},
         {'email':'g@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':True,
          'first_name':'g',
          'last_name':'g',
          'username':'g@mailinator.com'},
         {'email':'h@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':True,
          'first_name':'hoogly',
          'last_name':'h',
          'username':'h@mailinator.com'},
         ]

this_year = settings.CONSTITUENCY_YEAR
last_year = datetime.datetime(2009, 1, 1)
constituencies = [{'name':'Glasgow North',
                   'year':this_year,
                   'lat':53.2797662137,
                   'lon':-2.38760476605,
                   },
                  {'name':'Holborn and St Pancras',
                   'year':this_year,
                   'lat':53.2797662137,
                   'lon':-2.38760476605,
                   },
                  {'name':'Holborn & St Pancras',
                   'year':last_year,
                   'lat':53.2797662137,
                   'lon':-2.38760476605,
                   }]
        
class ViewsTestCase(TestCase):
    
    def setUp(self):
        self.users = []
        self.constituencies = []
        for item in constituencies:
            const = Constituency.objects.create(**item)
            const.save()
            self.constituencies.append(const)

    def _hack_confirm(self, userdict):
        user = CustomUser.objects.get(email=userdict['email'])
        user.is_active = True
        user.save()
            
    def test_viewing_different_models(self):
        """ Create a bunch of instance of models and view them """
        year = settings.CONSTITUENCY_YEAR
        def page_content(whole_content):
            # rough way of getting the HTML inside the div tag #page-content
            content = whole_content.split('id="main"')[1]
            return content
        
        def page_title(whole_content):
            return whole_content.split('<title>')[1].split('</title>')[0]
        
        response = self.client.get(self.constituencies[0].get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(cgi.escape(self.constituencies[0].name)\
                        in page_title(response.content))
        self.assertTrue(u"There are 0" in page_content(response.content))

        # add the first user
        response = self.client.post("/", users[0])
        self.assertEqual(response.status_code, 302)
        response = self.client.get("/", follow=True)
        self.assertContains(response, users[0]['first_name'])
        # no-one is active
        self.assertContains(response, "0 volunteers in 0")
        self._hack_confirm(users[0])
        response = self.client.get("/", follow=True)
        self.assertContains(response,
                            "1 volunteers in 1 constituencies (out of a total 2)")
        

        response = self.client.get("/add_constituency/")
        self.assertTrue(u"Join" in page_title(response.content))
        self.assertTrue(cgi.escape(self.constituencies[0].name) in page_content(response.content))
        
        response = self.client.get(self.constituencies[0].get_absolute_url())
        self.assertTrue(u"the only vol" in page_content(response.content))
        
        # add the second user
        response = self.client.get("/logout/", follow=True)
        response = self.client.post("/", users[1], follow=True)
        response = self.client.get("/", follow=True) # twice to skip
                                                     # invite step
        self._hack_confirm(users[1])
        response = self.client.get("/", follow=True) 
        self.assertTrue(users[1]['first_name'] in page_content(response.content))
        self.assertTrue("2 volunteers in 2 constituencies (out of a total 2)"\
                        in page_content(response.content))
        

        response = self.client.get("/add_constituency/")
        self.assertTrue(u"Join" in page_title(response.content))
        self.assertTrue(cgi.escape(self.constituencies[1].name) in page_content(response.content))
        
        response = self.client.get(self.constituencies[1].get_absolute_url())
        self.assertTrue(u"the only vol" in page_content(response.content))
        
        # and the third user
        response = self.client.get("/logout/", follow=True)
        response = self.client.post("/", users[2])
        response = self.client.get("/", follow=True) # twice to skip invite step
        self._hack_confirm(users[2])
        response = self.client.get("/", follow=True)
        self.assertTrue(users[2]['first_name'] in page_content(response.content))
        self.assertTrue("3 volunteers in 2 constituencies (out of a total 2)"\
                        in page_content(response.content))
        
        response = self.client.get("/add_constituency/")
        self.assertTrue(u"Join" in page_title(response.content))
        # constituencies[1] is the name in the current year
        self.assertTrue(cgi.escape(self.constituencies[1].name) in page_content(response.content))
        
        response = self.client.get(self.constituencies[1].get_absolute_url())
        self.assertTrue(u"2 vol" in page_content(response.content))
        

class TestSignup(TestCase):
    def test_validate_fields(self):
        """ Various field validations """
        crewe = Constituency.objects.create(
            name="Crewe and Nantwich",
            year = this_year)
        tests = [{'form':{},
                  'expect':'This field is required'},
                 {'form':{'email':'asdasd'},
                  'expect':'Enter a valid e-mail address'},
                 {'form':{'email':'321@mailinator.com',
                          'postcode':'asdasd'},
                  'expect':'Please enter a valid postcode'},
                 {'form':{'email':'321@mailinator.com',
                          'postcode':'cw16zz'},
                  'expect':'Unknown postcode'},
                 {'form':{'email':'321@mailinator.com',
                          'postcode':'cw16ar'},
                  'expect':'thanks for joining Democracy Club!'},]
        for test in tests:
            response = self.client.post("/", test['form'],
                                        follow=True)
            self.assertContains(response, test['expect'])

class TestAddConstituencies(TestCase):
    def setUp(self):
        crewe = Constituency.objects.create(
            name="Crewe & Nantwich",
            year = this_year)
        user = CustomUser.objects.create(
            username = "Frank",
            password = "",
            postcode = "CW1 6AR",
            can_cc = True)
        user.constituencies = [crewe]
        self.assert_(self.client.login(username="Frank", password=""))
        
    def test_postcode_search(self):
        """ User can enter a postcode into the search box to find a constituency. """
        # Example: a user in Crewe may search for a postcode in Hendon
        newcastle = Constituency.objects.create(
            name = "Hendon",
            year = this_year)
        self.assert_(self.client.login(username="Frank", password=""))
        # NW4 is in Hendon
        response = self.client.get("/add_constituency/#search", {"q":"NW4 3AS"})
        self.assertContains(response, "Hendon")

    def test_postcode_garbage(self):
        """ User could put garbage in the search box. this should not explode """
        response = self.client.get("/add_constituency/#search", {"q": u"\u2603"})
        # user is still registered in Crewe
        self.assertContains(response, "Crewe")
        # there is an error message
        self.assertContains(response, "can&#39;t find")
        
    def test_invalid_postcode(self):
        """ There are postcodes with valid formats that are not valid """
        response = self.client.get("/add_constituency/#search", {"q": u"D7 4XP"})
        # user is still registered in Crewe
        self.assertContains(response, "Crewe")
        # there is an error message
        self.assertContains(response, "can&#39;t find")

    def test_placename(self):
        """ User can also search for a placename """
        east_devon = Constituency.objects.create(
            name = "East Devon",
            year = this_year)
        response = self.client.get("/add_constituency/#search", {"q": u"Sidmouth"})
        # user is still registered in Crewe
        self.assertContains(response, "Crewe")
        self.assertContains(response, "Devon")

    def test_common_phrase(self):
        """ Should not explode if a common phrase is searched for e.g. 'North' """
        response = self.client.get("/add_constituency/#search", {"q": u"North"})
        self.assertContains(response, "Search for a constituency by place name or postcode")
        self.assertContains(response, "</html>") # page isn't truncated.


class TestLeaveAllConstituencies(TestCase):
    def runTest(self):
        """ Users can leave constituencies after they have joined them,
        potentually leaving them in no constituencies at all. """

        # user will sign up for Glasgow North
        Constituency.objects.create(
            name = "Glasgow North",
            year = this_year)

        # user signs up
        response = self.client.post("/",
            {'email':'foo@mailinator.com',
             'postcode':'G206BT',
             'can_cc':True,
             'first_name':'foo',
             'last_name':'bar'},
                                    follow=True)
        self.assertRedirects(response, "/welcome")

        # they have a constituency
        user = CustomUser.objects.get(email="foo@mailinator.com")
        self.assertEquals(1, len(user.current_constituencies))
        response = self.client.get("/add_constituency/")
        self.assertContains(response, "Glasgow North")

        # leaves their constituency
        response = self.client.get("/delete_constituency/glasgow-north/")
        self.assertEquals(0, len(user.current_constituencies)) 
        
        # should not go boom
        self.client.get("/add_constituency/")


class TestNorthernIreland(TestCase):
    """
    The twfy api is based on Borderline from the Ordinance Servay, and
    that does not cover Northern Ireland. Because support is patchy
    error cases are more common.
    """
    def test_add_consitiuency(self):
        # if registered in a Northern Irish constituency, can add more
        # constiuencies without error

        # Our user is registered in South Down
        south_down = Constituency.objects.create(
            name = "South Down",
            year = this_year)

        user = CustomUser.objects.create(
            username="foo",
            password="",
            email="foo@mailinator.com",
            postcode="BT30 8AH",
            first_name="foo",
            last_name="bar",
            can_cc=False)
        user.constituencies = [south_down]
        user.save()
        self.client.login(username="foo")
        response = self.client.get("/add_constituency/")

    def test_missing_neighbours(self):
        belfast_north = Constituency.objects.create(
            name = "Belfast North",
            year = this_year)
        belfast_north.save()
        south_down = Constituency.objects.create(
            name = "South Down",
            year = this_year)
        south_down.save()
        user = CustomUser.objects.create(
            username="foo",
            password="",
            email="foo@mailinator.com",
            postcode="BT30 8AH",
            first_name="foo",
            last_name="bar",
            can_cc=False)
        user.constituencies = [south_down]
        user.save()
        self.client.login(username="foo")
        response = self.client.get("/constituency/south-down/")

class TestBoundryPostcodes(TestCase):
    """
    Postcodes normlly fall unambiguously into one constituency.
    Sometimes they don't.
    """
    # See issue 28 for details
    def setUp(self):
        Constituency.objects.create(
            name = "Coventry North West",
            year = this_year)
        Constituency.objects.create(
            name = "Warwickshire North",
            year = this_year)
        # user signs up (this postcode lies on constituency border)
        response = self.client.post("/",
            {'email':'a@b.com',
             'postcode': 'CV7 8AH',
             'can_cc':True,
             'first_name':'foo',
             'last_name':'bar'})
        self.user = CustomUser.objects.get(email="a@b.com")

    def test_signup(self):
        # the constituency _should_ be North Warwickshire, but it's
        # wrong in OS Borderline
        self.assertEquals("Coventry North West",
                          self.user.constituencies.all()[0].name)

    def test_search(self):
        # user knows their constituency is wrong, and searches for the
        # correct constituency
        response = self.client.get("/add_constituency/#search",
                                   {"q": u"Warwickshire"})
        self.assertContains(response, "Warwickshire North")



class TestPlaceSearch(TestCase):
    """
    Test the constituency search box
    """
    def assertIn(self, obj, container, msg=None):
        if msg == None:
            msg = "%r not in %r" % (obj, container)
        self.assert_(obj in container, msg=msg)

    def setUp(self):
        constituencies = [
            "Coventry North West",
            "Warwickshire North",
            "Coventry North East",
            "Coventry South",
            "Meriden",
            "Nuneaton",
            "Rugby & Kenilworth",
            "Warwick & Leamington",
            ]
        for const in constituencies:
            Constituency.objects.create(
                name = const,
                year = this_year)

    def place_search(self, place):
        # makes output of views.place_search a bit easier to test.
        results = place_search(place)
        constituencies = []
        for fb, res in results:
            constituencies.extend(res)
        return [c.name for c in constituencies]

    def test1(self):
        # User may look for a constituency that is named after a town
        # in another constituency.

        # eg The town of Warwick is in Warwick & Lemington, but there
        # is a constituency called Warwickshire North. See issue 28
        # for details.
        self.assertIn("Warwickshire North",
                      self.place_search("Warwickshire"))

    def test2(self):
        # Nuneaton is both town and constituency
        # it should appear exactly once
        constituencies = self.place_search("Nuneaton")
        self.assertEquals(1, len(list(
                c for c in constituencies if c == "Nuneaton")))




class TestFlatPages(TestCase):
    FLAT_PAGES = [{'url':"/about/", 'title':"About", 'content':"This is a flat page"},
                  {'url':"/faq/", 'title':"FAQ", 'content':"This is another flat page"},]
    
    def setUp(self):
        site = Site.objects.get_current()
    
        for flat_page in self.FLAT_PAGES:
            page = FlatPage.objects.create(**flat_page)
            page.save()
            page.sites.add(site)
        
    def test_flatpage(self):
        """ Checks that flatpages work """
        response = self.client.get("/about/")
        self.assertContains(response, "About")
        self.assertContains(response, "This is a flat page")
        
    def test_flatpage_navigation(self):
        """ Test for issue 3 (navigation disappearing in flat page views) """
        response = self.client.get("/about/")
        self.assertContains(response, "FAQ")

        
class TestConstituencyMap(TestCase):
    def setUp(self):
        durham = Constituency.objects.create(
            name="City of Durham",
            year=this_year)
        crewe = Constituency.objects.create(
            name="Crewe & Nantwich",
            year=this_year)
        user = CustomUser.objects.create(
            username="Frank",
            password="",
            postcode="CW1 6AR",
            can_cc=True,
            is_active=True)
        user.constituencies = [crewe]
        self.assert_(self.client.login(username="Frank", password=""))
        
    def test_map(self):
        """ Checks that flatpages work """
        response = self.client.get("/statistics/heatmap.svg")
        self.assertContains(response, 'id="City_of_Durham" class="none')
        self.assertContains(response, 'id="Crewe_and_Nantwich" class="level1')
