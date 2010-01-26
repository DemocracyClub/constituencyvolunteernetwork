
from south.db import db
from django.db import models
from tasks.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Task'
        db.create_table('tasks_task', (
            ('id', orm['tasks.Task:id']),
            ('name', orm['tasks.Task:name']),
            ('email_subject', orm['tasks.Task:email_subject']),
            ('slug', orm['tasks.Task:slug']),
            ('project', orm['tasks.Task:project']),
            ('description', orm['tasks.Task:description']),
            ('email', orm['tasks.Task:email']),
            ('date_created', orm['tasks.Task:date_created']),
            ('decorator_class', orm['tasks.Task:decorator_class']),
        ))
        db.send_create_signal('tasks', ['Task'])
        
        # Adding model 'TaskUser'
        db.create_table('tasks_taskuser', (
            ('id', orm['tasks.TaskUser:id']),
            ('task', orm['tasks.TaskUser:task']),
            ('user', orm['tasks.TaskUser:user']),
            ('constituency', orm['tasks.TaskUser:constituency']),
            ('state', orm['tasks.TaskUser:state']),
            ('date_assigned', orm['tasks.TaskUser:date_assigned']),
            ('date_modified', orm['tasks.TaskUser:date_modified']),
            ('url', orm['tasks.TaskUser:url']),
            ('post_url', orm['tasks.TaskUser:post_url']),
            ('emails_sent', orm['tasks.TaskUser:emails_sent']),
        ))
        db.send_create_signal('tasks', ['TaskUser'])
        
        # Adding model 'Badge'
        db.create_table('tasks_badge', (
            ('id', orm['tasks.Badge:id']),
            ('name', orm['tasks.Badge:name']),
            ('task', orm['tasks.Badge:task']),
            ('user', orm['tasks.Badge:user']),
            ('date_awarded', orm['tasks.Badge:date_awarded']),
            ('number', orm['tasks.Badge:number']),
        ))
        db.send_create_signal('tasks', ['Badge'])
        
        # Adding model 'Project'
        db.create_table('tasks_project', (
            ('id', orm['tasks.Project:id']),
            ('name', orm['tasks.Project:name']),
            ('slug', orm['tasks.Project:slug']),
            ('description', orm['tasks.Project:description']),
            ('url', orm['tasks.Project:url']),
        ))
        db.send_create_signal('tasks', ['Project'])
        
        # Adding model 'ConstituencyCompletenessTask'
        db.create_table('tasks_task', (
            
        ))
        db.send_create_signal('tasks', ['ConstituencyCompletenessTask'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Task'
        db.delete_table('tasks_task')
        
        # Deleting model 'TaskUser'
        db.delete_table('tasks_taskuser')
        
        # Deleting model 'Badge'
        db.delete_table('tasks_badge')
        
        # Deleting model 'Project'
        db.delete_table('tasks_project')
        
        # Deleting model 'ConstituencyCompletenessTask'
        db.delete_table('tasks_task')
        
    
    
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
            'decorator_class': ('django.db.models.fields.CharField', [], {'max_length': '180'}),
            'description': ('django.db.models.fields.TextField', [], {}),
            'email': ('django.db.models.fields.TextField', [], {}),
            'email_subject': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '80'}),
            'project': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Project']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '80', 'db_index': 'True'}),
            'users': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['signup.CustomUser']"})
        },
        'tasks.taskuser': {
            'constituency': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.Constituency']", 'null': 'True', 'blank': 'True'}),
            'date_assigned': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'date_modified': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'emails_sent': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'post_url': ('django.db.models.fields.CharField', [], {'max_length': '2048', 'null': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.SmallIntegerField', [], {}),
            'task': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['tasks.Task']"}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '2048'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['signup.CustomUser']"})
        }
    }
    
    complete_apps = ['tasks']
