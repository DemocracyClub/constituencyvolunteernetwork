from django.contrib import admin

from reversion.admin import VersionAdmin

import models

class IssueAdmin(VersionAdmin):
    list_display = ('question',
                    'constituency',
                    'created_by',
                    'status')
    list_filter = ('status',)

admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.RefinedIssue)
