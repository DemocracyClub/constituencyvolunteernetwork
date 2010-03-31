from django.contrib import admin

from reversion.admin import VersionAdmin

import models

class IssueAdmin(VersionAdmin):
    list_display = ('question',
                    'constituency',
                    'created_by',
                    'status')
    list_filter = ('status',)
    search_fields = ('question', 'created_by__email','last_updated_by',)

class RefinedIssueAdmin(admin.ModelAdmin):
    list_display = ('question',
                    'constituency',
                    'moderator',)
    search_fields = ('question', 'moderator',)

admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.RefinedIssue, RefinedIssueAdmin)

