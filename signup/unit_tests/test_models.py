# python
import datetime

# django
from django.conf import settings

# app
from testbase import TestCase

from signup import models
from signup.models import Constituency, CustomUser

this_year = settings.CONSTITUENCY_YEAR
last_year = settings.CONSTITUENCY_YEAR - datetime.timedelta(365)

CONSTITUENCIES = [{'name':'My place',
                   'year': this_year},
                  {'name':'My other place',
                   'year': this_year},
                  {'name':'My place last year',
                   'year': last_year},]

USERS = [{'email':'f@mailinator.com',
          'postcode':'G206BT',
          'can_cc':True,
          'first_name':'f',
          'last_name':'f',
          'username':'f@mailinator.com',
          'is_active':True},
         {'email':'g@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':True,
          'first_name':'g',
          'last_name':'g',
          'username':'g@mailinator.com',
          'is_active':True},
         {'email':'h@mailinator.com',
          'postcode':'WC2H8DN',
          'can_cc':True,
          'first_name':'h',
          'last_name':'h',
          'username':'h@mailinator.com',
          'is_active':False},
         ]

class ModelsTestCase(TestCase):

    def setUp(self):
        # create a sector
        self.constituencies = []
        self.users = []
        for c in CONSTITUENCIES:    
            const = Constituency.objects.create(**c)
            const.save()
            self.constituencies.append(const)

        for u in USERS:    
            user = CustomUser.objects.create(**u)
            user.is_active = u['is_active']
            user.save()
            self.users.append(user)        
            
    def test_basic_instance_creation(self):
        """test to make sure the various models can be created"""
        first = self.constituencies[0]
        self.assertEqual(first.slug, 'my-place')
        self.assertEqual(first.get_absolute_url(),
                         u"/constituency/%s/" % first.slug)
        count = 0
        for user in self.users:
            self.assertEqual(user.postcode, USERS[count]['postcode'])
            count += 1
            
    def test_different_dates(self):
        self.users[0].constituencies.add(self.constituencies[0])
        self.users[0].constituencies.add(self.constituencies[2])
        self.assertEqual(self.users[0].current_constituencies.count(), 1)
        

    def test_filter_constituency_by_user(self):
        empty = models.filter_where_customuser_fewer_than(1)
        self.assertEqual(len(empty), 2)
        # add an inactive user.  Shouldn't make a difference
        self.users[2].constituencies.add(self.constituencies[0])
        empty = models.filter_where_customuser_fewer_than(1)
        
        self.assertEqual(len(empty), 2)
        
        self.users[1].constituencies.add(self.constituencies[0])
        empty = models.filter_where_customuser_fewer_than(1)
        self.assertEqual(len(empty), 1)

        more = models.filter_where_customuser_more_than(0)
        self.assertEqual(len(more), 1)

class TestNeigbours(TestCase):
    # constituency names must match those returned from twfy
    data = [{"name" : "Chipping Barnet",
             "lat" : 51.6395895436,
             "lon" : -0.192217329457,
             "year": this_year
             },
            {"name" : "Hendon",
             "lat" : 51.606570454,
             "lon" : -0.252407672041,
             "year": this_year
             },
            {"name" : "Altrincham & Sale West",
             "lat" : 53.3989495951,
             "lon" : -2.38207857643,
             "year": this_year
             },
            {"name" : "Hertsmere",
             "lat" : 51.6802918234,
             "lon" : -0.274986273182,
             "year": this_year
             },
            
            {"name" : "Stretford & Urmston",
             "lat" : 53.4450638328,
             "lon" : -2.35374956251,
             "year": this_year
             },
            {"name" : "Tatton",
             "lat" : 53.2797662137,
             "lon" : -2.38760476605,
             "year": this_year
            },
            {"name" : "Belfast North",
             "year": this_year
            }]

    def setUp(self):
        for c in self.data:
            Constituency.objects.create(**c)

    def test_center(self):
        place = Constituency.objects.get(name="Altrincham & Sale West")
        self.assertEqual((53.3989495951, -2.38207857643),
                         (place.lat, place.lon))

    def test_neigbours(self):
        # Stirling's neighbouring constituencies are Falkirk and West
        # Dunbartonshire. Hendon is a long way away
        centre = Constituency.objects.get(name="Chipping Barnet")
        names = (c.name for c in centre.neighbors(limit=3))
        self.assertEqual(list(names), ["Hendon", "Hertsmere", "Tatton"])

        centre = Constituency.objects.get(name="Altrincham & Sale West")
        names = (c.name for c in centre.neighbors(limit=3))
        self.assertEqual(list(names), ["Stretford & Urmston",
                                       "Tatton", "Hertsmere"])
        
        subset = Constituency.objects.filter(name__in=["Tatton",
                                                       "Hendon"])
        centre = subset[0]
        import pdb; pdb.set_trace()
        self.assertEqual(subset[1],
                         centre.neighbors(constituency_set=subset)[0])
