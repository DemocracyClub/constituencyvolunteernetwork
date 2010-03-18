from django.contrib import admin

import models

class CommentAdmin(admin.ModelAdmin):
    list_display = ('submit_date', 'user', 'comment', 'is_public', 'removal_reason')
    list_filter = ('is_public', 'is_removed')
    search_fields = ('user__email',)

class NotifyCommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'constituency', 'notify_type', 'created_at')
    list_filter = ('notify_type',)
    search_fields = ('user__email', 'constituency__name')    

admin.site.register(models.CommentSimple, CommentAdmin)
admin.site.register(models.NotifyComment, NotifyCommentAdmin)



