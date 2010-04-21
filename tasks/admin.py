from django.contrib import admin

import models


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }

class TaskUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'state', 'constituency')
    list_filter = ('task','state','constituency')
    search_fields = ('user__email',)

class TaskEmailAdmin(admin.ModelAdmin):
    list_display = ('subject', 'email_type', 'task', 'date_last_sent', 'opened')
    exclude = ('taskusers', 'date_last_sent', 'opened')
    list_filter = ('task',)

class TaskEmailUserAdmin(admin.ModelAdmin):
    list_display = ('task_user', 'task_email', 'date_added', 'date_sent')
    list_filter = ('date_sent',)
    search_fields = ('user__email',)

admin.site.register(models.TaskUser, TaskUserAdmin)
admin.site.register(models.TaskEmail, TaskEmailAdmin)
admin.site.register(models.TaskEmailUser, TaskEmailUserAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Badge)
