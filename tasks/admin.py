from django.contrib import admin

import models


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }

class TaskUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'state', 'constituency')
    list_filter = ('task','state','constituency')
    search_fields = ('user',)

admin.site.register(models.TaskUser, TaskUserAdmin)
admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.Badge)
