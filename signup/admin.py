from django.contrib import admin

import models    

class ConstituencyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'is_active', 'last_login')
    list_filter = ('constituencies','is_active')
    search_fields = ('first_name', 'last_name', 'email')

    def show_activation_url(self, request, queryset):
        message = ""
        for custom_user in queryset:
            registrationprofile = custom_user.registrationprofile_set.get()
            message = message + "Activation URL for " + custom_user.display_name + ": " + registrationprofile.get_activation_url()
        self.message_user(request, message)
    show_activation_url.short_description = "Show activation URL for selected users"

    def show_login_url(self, request, queryset):
        message = ""
        for custom_user in queryset:
            registrationprofile = custom_user.registrationprofile_set.get()
            message = message + "Login URL for " + custom_user.display_name + ": " + registrationprofile.get_login_url()
        self.message_user(request, message)
    show_login_url.short_description = "Show login URL for selected users"

    actions = ['show_activation_url', 'show_login_url']

admin.site.register(models.Constituency, ConstituencyAdmin)
admin.site.register(models.CustomUser, CustomUserAdmin)
