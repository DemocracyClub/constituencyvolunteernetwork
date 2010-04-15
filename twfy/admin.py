from django.contrib import admin

import models

class SurveyInviteAdmin(admin.ModelAdmin):
    search_fields = ('candidacy__candidate__name',)

admin.site.register(models.SurveyInvite, SurveyInviteAdmin)
