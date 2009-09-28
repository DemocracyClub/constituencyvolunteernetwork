from django.contrib import admin

import models

class PartyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}
    list_display = ('name', 'slug')

class CandidateAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}
    list_display = ('name', 'constituency', 'party', )


admin.site.register(models.Candidate, CandidateAdmin)
admin.site.register(models.Party, PartyAdmin)
