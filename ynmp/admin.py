from django.contrib import admin

import models

class YNMPActionAdmin(admin.ModelAdmin):
    list_display = ('user', 'task', 'date', 'summary')
    list_filter = ('task',)
    search_fields = ('user__email', 'task')

class YNMPConstituencyAdmin(admin.ModelAdmin):
    pass

class CandidateAdmin(admin.ModelAdmin):
    list_display = ('ynmp_id', 'name', 'email', 'party',)
    search_fields = ('name','party')

class CandidacyAdmin(admin.ModelAdmin):
    list_display = ('ynmp_id', 'ynmp_constituency', 'candidate',)

class PartyAdmin(admin.ModelAdmin):
    list_display = ('ynmp_id', 'name',)
    search_fields = ('name',)


admin.site.register(models.YNMPAction, YNMPActionAdmin)
admin.site.register(models.YNMPConstituency, YNMPConstituencyAdmin)
admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.Candidacy, CandidacyAdmin)
admin.site.register(models.Party, PartyAdmin)

