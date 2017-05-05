from django.apps import AppConfig
from django import forms
from django.contrib import admin
from .models import UserProfile
# Register your models here.

class AccountsConfig(AppConfig):
    name = 'accounts'
    verbose_name = "用户资料"


class AccountsAdminForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('user', 'nikename', 'email', 'gender', 'phone', 'qq_number', 'birthday',
        	'self_intro', 'photo')


class AccountsAdmin(admin.ModelAdmin):
	form = AccountsAdminForm

admin.site.register(UserProfile, AccountsAdmin)