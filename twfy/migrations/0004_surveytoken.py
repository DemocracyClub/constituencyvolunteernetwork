
from south.db import db
from django.db import models
from twfy.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'SurveyInvite.survey_token'
        db.add_column('twfy_surveyinvite', 'survey_token', orm['twfy.surveyinvite:survey_token'])
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'SurveyInvite.survey_token'
        db.delete_column('twfy_surveyinvite', 'survey_token')
        
    
    
    models = {
        'signup.constituency': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80', 'db_index': 'True'}),
            'year': ('django.db.models.fields.DateField', [], {})
        },
        'twfy.surveyinvite': {
            'candidacy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ynmp.Candidacy']", 'null': 'True', 'blank': 'True'}),
            'emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'filled_in': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'pester_emails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'survey_token': ('django.db.models.fields.CharField', [], {'max_length': '30', 'null': 'True', 'blank': 'True'}),
            'ynmp_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'ynmp.candidacy': {
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ynmp.Candidate']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ynmp_constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ynmp.YNMPConstituency']"}),
            'ynmp_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'})
        },
        'ynmp.candidate': {
            'code': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'dob': ('django.db.models.fields.CharField', [], {'max_length': '16', 'null': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'party': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ynmp.Party']", 'null': 'True', 'blank': 'True'}),
            'phone': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'university': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'updated': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'ynmp_id': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'ynmp_party_id': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'})
        },
        'ynmp.party': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_id': ('django.db.models.fields.CharField', [], {'max_length': '9', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ynmp_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        },
        'ynmp.ynmpconstituency': {
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.Constituency']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ynmp_seat_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        }
    }
    
    complete_apps = ['twfy']
