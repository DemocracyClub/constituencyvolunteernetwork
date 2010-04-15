
from south.db import db
from django.db import models
from ynmp.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Party'
        db.create_table('ynmp_party', (
            ('id', orm['ynmp.party:id']),
            ('ynmp_id', orm['ynmp.party:ynmp_id']),
            ('name', orm['ynmp.party:name']),
        ))
        db.send_create_signal('ynmp', ['Party'])
        
        # Adding model 'Candidate'
        db.create_table('ynmp_candidate', (
            ('id', orm['ynmp.candidate:id']),
            ('ynmp_id', orm['ynmp.candidate:ynmp_id']),
            ('status', orm['ynmp.candidate:status']),
            ('email', orm['ynmp.candidate:email']),
            ('updated', orm['ynmp.candidate:updated']),
            ('gender', orm['ynmp.candidate:gender']),
            ('code', orm['ynmp.candidate:code']),
            ('university', orm['ynmp.candidate:university']),
            ('name', orm['ynmp.candidate:name']),
            ('phone', orm['ynmp.candidate:phone']),
            ('dob', orm['ynmp.candidate:dob']),
            ('ynmp_party_id', orm['ynmp.candidate:ynmp_party_id']),
            ('party', orm['ynmp.candidate:party']),
        ))
        db.send_create_signal('ynmp', ['Candidate'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Party'
        db.delete_table('ynmp_party')
        
        # Deleting model 'Candidate'
        db.delete_table('ynmp_candidate')
        
    
    
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
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seen_invite': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'unsubscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
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
        },
        'ynmp.ynmpaction': {
            'candidate_code': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'candidate_name': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'date': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'details_added': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'party_name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'points_awarded': ('django.db.models.fields.IntegerField', [], {}),
            'summary': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'task': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.CustomUser']"})
        }
    }
    
    complete_apps = ['ynmp']
