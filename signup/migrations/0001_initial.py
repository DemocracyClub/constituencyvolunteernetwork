
from south.db import db
from django.db import models
from signup.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'RegistrationProfile'
        db.create_table('signup_registrationprofile', (
            ('id', orm['signup.RegistrationProfile:id']),
            ('user', orm['signup.RegistrationProfile:user']),
            ('email', orm['signup.RegistrationProfile:email']),
            ('activation_key', orm['signup.RegistrationProfile:activation_key']),
            ('activated', orm['signup.RegistrationProfile:activated']),
        ))
        db.send_create_signal('signup', ['RegistrationProfile'])
        
        # Adding model 'Constituency'
        db.create_table('signup_constituency', (
            ('id', orm['signup.Constituency:id']),
            ('name', orm['signup.Constituency:name']),
            ('slug', orm['signup.Constituency:slug']),
            ('lat', orm['signup.Constituency:lat']),
            ('lon', orm['signup.Constituency:lon']),
            ('year', orm['signup.Constituency:year']),
        ))
        db.send_create_signal('signup', ['Constituency'])
        
        # Adding model 'CustomUser'
        db.create_table('signup_customuser', (
            ('user_ptr', orm['signup.CustomUser:user_ptr']),
            ('postcode', orm['signup.CustomUser:postcode']),
            ('can_cc', orm['signup.CustomUser:can_cc']),
            ('login_count', orm['signup.CustomUser:login_count']),
            ('seen_invite', orm['signup.CustomUser:seen_invite']),
        ))
        db.send_create_signal('signup', ['CustomUser'])
        
        # Adding ManyToManyField 'CustomUser.constituencies'
        db.create_table('signup_customuser_constituencies', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('customuser', models.ForeignKey(orm.CustomUser, null=False)),
            ('constituency', models.ForeignKey(orm.Constituency, null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'RegistrationProfile'
        db.delete_table('signup_registrationprofile')
        
        # Deleting model 'Constituency'
        db.delete_table('signup_constituency')
        
        # Deleting model 'CustomUser'
        db.delete_table('signup_customuser')
        
        # Dropping ManyToManyField 'CustomUser.constituencies'
        db.delete_table('signup_customuser_constituencies')
        
    
    
    models = {
        'auth.group': {
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
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
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
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
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seen_invite': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'signup.registrationprofile': {
            'activated': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'activation_key': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.CustomUser']"})
        }
    }
    
    complete_apps = ['signup']
