from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', '男'),
        ('F', '女'),
    )
    user = models.OneToOneField(User, unique=True)
    nikename = models.CharField(blank=True, max_length=20, verbose_name='昵称')
    email = models.EmailField(blank=True, verbose_name='电子邮箱')
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES, verbose_name='性别')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号码')
    qq_number = models.CharField(max_length=20, blank=True, verbose_name='QQ号码')
    birthday = models.DateField(blank=True, null=True, verbose_name='生日')
    self_intro = models.TextField(blank=True, verbose_name='自我介绍')
    photo = models.ImageField(upload_to='accounts/', blank=True, null=True, verbose_name='头像')

    def __str__(self):
        return 'User Profile for :' + self.user.username


class UserAddress(models.Model):
    user = models.ForeignKey(User)
    receiver_name = models.CharField(max_length=20, verbose_name='收货人姓名')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货人电话')
    province = models.CharField(max_length=20, verbose_name='省份')
    city = models.CharField(max_length=20, verbose_name='城市')
    area = models.CharField(max_length=20, verbose_name='地区')
    detail_addr = models.TextField(verbose_name='详细地址')
    post_code = models.CharField(max_length=10, verbose_name='邮编')

    def __str__(self):
        return 'Address, from ' + self.user.username + ' send to ' + self.receiver_name
