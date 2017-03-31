from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    user = models.ForeignKey(User, unique=True)
    email = models.EmailField(blank=True, verbose_name='电子邮箱')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='性别')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号码')
    qq_number = models.CharField(max_length=20, blank=True, verbose_name='QQ号码')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    self_intro = models.TextField(blank=True, verbose_name='自我介绍')
    photo = models.ImageField(upload_to='accounts/', blank=True, verbose_name='头像')

    def __str__(self):
        return 'User Profile for :' + self.user.username


