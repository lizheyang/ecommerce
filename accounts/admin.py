from django.apps import AppConfig
from django import forms
from django.contrib import admin
from .models import UserProfile, UserFeedback
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


class FeedbackAdminForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        exclude = ('created_at',)


class FeedbackAdmin(admin.ModelAdmin):
    fields = ('id', 'user', 'title', 'content', 'reply', 'status_code')
    readonly_fields = ('id', 'user', 'title', 'content')
    form = FeedbackAdminForm

admin.site.register(UserProfile, AccountsAdmin)
admin.site.register(UserFeedback, FeedbackAdmin)