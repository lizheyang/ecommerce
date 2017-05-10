from django import forms
from .models import UserProfile, UserAddress, UserFeedback


class UserProfileForm(forms.ModelForm):
    # TODO:定制表格
    # GENDER_CHOICES = (
    #     ('M', '男'),
    #     ('F', '女'),
    # )
    # gender = forms.ChoiceField(choices=GENDER_CHOICES, label='性别')
    # phone = forms.CharField(label='手机号码')
    # qq_number = forms.CharField(label='QQ号')
    # birthday = forms.DateField(label='生日')
    # self_info = forms.CharField(label='个人介绍', widget=forms.Textarea)
    # photo = forms.ImageField(label='头像')
    class Meta:
        model = UserProfile
        exclude = ('user', )


class UserAddressForm(forms.ModelForm):
    class Meta:
        model = UserAddress
        exclude = ('user',)


class UserFeedbackForm(forms.ModelForm):
    class Meta:
        model = UserFeedback
        exclude = ('user', 'reply', 'created_at', 'status_code')


