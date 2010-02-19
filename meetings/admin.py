from django.contrib import admin

import models

class MeetingInterestAdmin(admin.ModelAdmin):
    list_display = ('user', 'postcode', 'organiser', 'date')
    list_filter = ('organiser',)
    search_fields = ('user__email','postcode')

admin.site.register(models.MeetingInterest, MeetingInterestAdmin)
