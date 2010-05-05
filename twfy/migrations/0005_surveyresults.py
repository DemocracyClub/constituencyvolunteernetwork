
from south.db import db
from django.db import models
from twfy.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Statement'
        db.create_table('twfy_statement', (
            ('id', orm['twfy.statement:id']),
            ('twfy_key', orm['twfy.statement:twfy_key']),
            ('refined_issue', orm['twfy.statement:refined_issue']),
            ('question', orm['twfy.statement:question']),
            ('national', orm['twfy.statement:national']),
        ))
        db.send_create_signal('twfy', ['Statement'])
        
        # Adding model 'SurveyResponse'
        db.create_table('twfy_surveyresponse', (
            ('id', orm['twfy.surveyresponse:id']),
            ('candidacy', orm['twfy.surveyresponse:candidacy']),
            ('statement', orm['twfy.surveyresponse:statement']),
            ('national', orm['twfy.surveyresponse:national']),
            ('agreement', orm['twfy.surveyresponse:agreement']),
            ('more_explanation', orm['twfy.surveyresponse:more_explanation']),
        ))
        db.send_create_signal('twfy', ['SurveyResponse'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Statement'
        db.delete_table('twfy_statement')
        
        # Deleting model 'SurveyResponse'
        db.delete_table('twfy_surveyresponse')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80', 'unique': 'True'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'unique_together': "(('content_type', 'codename'),)"},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True', 'blank': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'max_length': '30', 'unique': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'unique_together': "(('app_label', 'model'),)", 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'issue.issue': {
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.Constituency']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'created_by': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.CustomUser']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_updated_by': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'issues_last_updater'", 'null': 'True', 'to': "orm['signup.CustomUser']"}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '20'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'issue.refinedissue': {
            'based_on': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'refined'", 'to': "orm['issue.Issue']"}),
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.Constituency']"}),
            'created_at': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fine_tuned': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'moderator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'moderated_issues'", 'to': "orm['signup.CustomUser']"}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'rating': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'reference_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'approve'", 'max_length': '20'}),
            'updated_at': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'signup.constituency': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lat': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'lon': ('django.db.models.fields.FloatField', [], {'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80', 'db_index': 'True'}),
            'year': ('django.db.models.fields.DateField', [], {})
        },
        'signup.customuser': {
            'can_cc': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'constituencies': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['signup.Constituency']"}),
            'display_name': ('django.db.models.fields.CharField', [], {'default': "'Someone'", 'max_length': '30'}),
            'hassling': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seen_invite': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'unsubscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'twfy.statement': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'national': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'question': ('django.db.models.fields.CharField', [], {'max_length': '350', 'null': 'True', 'blank': 'True'}),
            'refined_issue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['issue.RefinedIssue']", 'null': 'True', 'blank': 'True'}),
            'twfy_key': ('django.db.models.fields.CharField', [], {'max_length': '20'})
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
        'twfy.surveyresponse': {
            'agreement': ('django.db.models.fields.IntegerField', [], {}),
            'candidacy': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['ynmp.Candidacy']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'more_explanation': ('django.db.models.fields.TextField', [], {}),
            'national': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'statement': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['twfy.Statement']"})
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
            'nomination_url': ('django.db.models.fields.URLField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'nominations_entered': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'ynmp_seat_id': ('django.db.models.fields.CharField', [], {'max_length': '9'})
        }
    }
    
    complete_apps = ['twfy']
