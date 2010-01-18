from django.contrib import admin

import models

class IssueAdmin(admin.ModelAdmin):
    list_display = ('question', 'reference_url', 'constituency', 'created_by')

admin.site.register(models.Issue, IssueAdmin)

