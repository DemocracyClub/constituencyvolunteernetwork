
from south.db import db
from django.db import models
from tasks.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Deleting field 'TaskEmail.task_user_state'
        db.delete_column('tasks_taskemail', 'task_user_state')
        
        # Changing field 'TaskEmailUser.date_sent'
        # (to signature: django.db.models.fields.DateTimeField(null=True, blank=True))
        db.alter_column('tasks_taskemailuser', 'date_sent', orm['tasks.taskemailuser:date_sent'])
        
    
    
    def backwards(self, orm):
        
        # Adding field 'TaskEmail.task_user_state'
        db.add_column('tasks_taskemail', 'task_user_state', orm['tasks.taskemail:task_user_state'])
        
        # Changing field 'TaskEmailUser.date_sent'
        # (to signature: django.db.models.fields.DateTimeField(null=True))
        db.alter_column('tasks_taskemailuser', 'date_sent', orm['tasks.taskemailuser:date_sent'])
        
    
    
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
            'display_name': ('django.db.models.fields.CharField', [], {'default': "'Someone'", 'max_length': '30'}),
            'login_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'postcode': ('django.db.models.fields.CharField', [], {'max_length': '9'}),
            'seen_invite': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'unsubscribed': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'blank': 'True'}),
            'user_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['auth.User']", 'unique': 'True', 'primary_key': 'True'})
        },
        'tasks.badge': {
            'date_awarded': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'number': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.CustomUser']"})
        },
        'tasks.project': {
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80', 'db_index': 'True'}),
            'url': ('django.db.models.fields.URLField', [], {'max_length': '200'})
        },
        'tasks.task': {
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'decorator_class': ('django.db.models.fields.CharField', [], {'max_length': '180', 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Project']"}),
            'short_description': ('django.db.models.fields.TextField', [], {}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80', 'db_index': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['signup.CustomUser']"})
        },
        'tasks.taskemail': {
            'body': ('django.db.models.fields.TextField', [], {}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'date_created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_last_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'email_type': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'opened': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'queue': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tasks.TaskUser']"}),
            'subject': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'default': 'None', 'to': "orm['tasks.Task']", 'null': 'True'}),
            'taskusers': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['tasks.TaskUser']", 'null': 'True', 'blank': 'True'})
        },
        'tasks.taskemailuser': {
            'date_added': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_sent': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'task_email': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.TaskEmail']"}),
            'task_user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.TaskUser']"})
        },
        'tasks.taskuser': {
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.Constituency']", 'null': 'True', 'blank': 'True'}),
            'date_assigned': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_url': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'source_email': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.TaskEmail']", 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.CustomUser']"})
        }
    }
    
    complete_apps = ['tasks']
