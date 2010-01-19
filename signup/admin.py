import re

from django.contrib import admin
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

import models

REGEX = re.compile(r'^.*$', re.U)

class MyUserChangeForm(UserChangeForm):
    username = forms.RegexField(
        label='Username', 
        max_length=30, 
        regex=REGEX,
        help_text = 'Required. 30 characters or fewer. Alphanumeric characters only (letters, digits, hyphens and underscores).',
        error_message = 'This value must contain only letters, numbers, hyphens and underscores.')
  
    password = forms.CharField(required=False)

    class Meta:
        model = User
        exclude = ('password',)

class MyCustomUserChangeForm(UserChangeForm):
    username = forms.RegexField(
        label='Username', 
        max_length=30, 
        regex=REGEX,
        help_text = 'Required. 30 characters or fewer. Alphanumeric characters only (letters, digits, hyphens and underscores).',
        error_message = 'This value must contain only letters, numbers, hyphens and underscores.')
  
    password = forms.CharField(required=False)

    class Meta:
        model = models.CustomUser
        exclude = ('password',)

class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm

admin.site.unregister(User)
admin.site.register(User, MyUserAdmin)

class ConstituencyAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('name',),}

class CustomUserAdmin(admin.ModelAdmin):
    form = MyCustomUserChangeForm
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
