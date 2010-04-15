
from south.db import db
from django.db import models
from twfy.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'SurveyInvite'
        db.create_table('twfy_surveyinvite', (
            ('id', orm['twfy.SurveyInvite:id']),
            ('ynmp_id', orm['twfy.SurveyInvite:ynmp_id']),
            ('candidate', orm['twfy.SurveyInvite:candidate']),
            ('emailed', orm['twfy.SurveyInvite:emailed']),
            ('filled_in', orm['twfy.SurveyInvite:filled_in']),
        ))
        db.send_create_signal('twfy', ['SurveyInvite'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'SurveyInvite'
        db.delete_table('twfy_surveyinvite')
        
    
    
    models = {
        'twfy.surveyinvite': {
            'candidate': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ynmp.Candidate']"}),
            'emailed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'filled_in': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ynmp_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
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
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'ynmp_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        }
    }
    
    complete_apps = ['twfy']
