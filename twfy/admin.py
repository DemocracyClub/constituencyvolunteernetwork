from django.contrib import admin

import models

class SurveyInviteAdmin(admin.ModelAdmin):
    list_display = ('candidacy', 'filled_in', 'pester_emails_sent')

    search_fields = ('candidacy__candidate__name',)

admin.site.register(models.SurveyInvite, SurveyInviteAdmin)
