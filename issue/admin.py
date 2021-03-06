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


class RefinedIssueAdmin(VersionAdmin):
    list_display = ('question',
                    'constituency',
                    'based_on',
                    'moderator',
                    'updated_at',
                    'created_at')
    list_filter = ('moderator',)
    search_fields = ('question', 'moderator__email')


class ConstituencyIssueCompletionAdmin(VersionAdmin):
    list_display = ('constituency',
                    'number_to_moderate',
                    'number_to_completion',
                    'completed')
    list_filter = ('completed',)

admin.site.register(models.Issue, IssueAdmin)
admin.site.register(models.RefinedIssue, RefinedIssueAdmin)
admin.site.register(models.ConstituencyIssueCompletion,
                    ConstituencyIssueCompletionAdmin)
