from django.contrib import admin

import models


class CommentAdmin(admin.ModelAdmin):
    list_display = ('submit_date', 'user', 'comment', 'is_public')
    list_filter = ('is_public', 'is_removed')
    search_fields = ('user__email',)    

admin.site.register(models.CommentSimple, CommentAdmin)
admin.site.register(models.NotifyComment)



