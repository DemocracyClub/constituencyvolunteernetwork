
from south.db import db
from django.db import models
from issue.models import *

class Migration:
    
    def forwards(self, orm):
        # There's no standard support for unique constaints over multiple
        # columns, so we do it with custom SQL
        db.execute('create unique index signup_constituency_name_year_idx on signup_constituency (name, year)')
    
    def backwards(self, orm):
        db.execute('drop index signup_constituency_name_year_idx')
