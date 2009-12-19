from django.contrib import admin

import models


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


class TaskAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',), }


admin.site.register(models.Project, ProjectAdmin)
admin.site.register(models.Task, TaskAdmin)
admin.site.register(models.TaskUser)
admin.site.register(models.Badge)
