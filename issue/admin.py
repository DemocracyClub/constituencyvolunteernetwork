from django.contrib import admin

from reversion.admin import VersionAdmin

import models

class IssueAdmin(VersionAdmin):
    list_display = ('question',
                    'constituency',
                    'created_by',
                    'status')
    list_filter = ('status',)
    search_fields = ('question', 'created_by__email')

admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.RefinedIssue)
