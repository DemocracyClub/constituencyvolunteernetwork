from django.contrib import admin

from reversion.admin import VersionAdmin

import models

class IssueAdmin(VersionAdmin):
    list_display = ('question', 'reference_url', 'constituency', 'created_by', 'status')

admin.site.register(models.Issue, IssueAdmin)

