from django.contrib import admin

import models

class MeetingInterestAdmin(admin.ModelAdmin):
    search_fields = ('user__email', 'postcode')

admin.site.register(models.MeetingInterest, MeetingInterestAdmin)
