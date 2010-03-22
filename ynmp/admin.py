from django.contrib import admin

import models

class YNMPActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'date', 'summary')
    list_filter = ('task',)
    search_fields = ('user__email', 'task')

admin.site.register(models.YNMPAction, YNMPActionAdmin)

