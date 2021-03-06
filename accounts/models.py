from django.db import models
from django.contrib.auth.models import User
from catalog.models import Product
from menus.models import Menu


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

    class Meta:
        app_label = 'accounts'
        verbose_name = '用户资料'
        verbose_name_plural = '用户资料'

    def __str__(self):
        return 'User Profile for :' + self.user.username


class UserAddress(models.Model):
    user = models.ForeignKey(User)
    receiver_name = models.CharField(max_length=20, verbose_name='收货人姓名')
    receiver_phone = models.CharField(max_length=20, verbose_name='收货人电话')
    province = models.CharField(max_length=20, verbose_name='省份')
    city = models.CharField(max_length=20, verbose_name='城市')
    area = models.CharField(max_length=20, verbose_name='地区')
    detail_addr = models.CharField(max_length=70, verbose_name='详细地址')
    post_code = models.CharField(max_length=10, verbose_name='邮编')

    class Meta:
        app_label = 'accounts'

    def __str__(self):
        return '地址，收货人为 ' + str(self.receiver_name)


class UserCollection(models.Model):
    menu = models.ForeignKey(Menu, null=True)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'accounts'
        verbose_name = '菜单收藏'
        verbose_name_plural = '菜单收藏'

    def __str__(self):
        return self.user.username + '收藏的：' + self.menu.name


class UserFeedback(models.Model):
    STATUS = (
        (1, '未回复'),
        (2, '已回复'),
    )
    user = models.ForeignKey(User)
    title = models.CharField(max_length=50,verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    reply = models.TextField(verbose_name='回复', blank=True, null=True)
    status_code = models.IntegerField(choices=STATUS, default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'accounts'
        verbose_name = '用户反馈'
        verbose_name_plural = '用户反馈'
        ordering = ['-created_at']

    def __str__(self):
        return '用户' + self.user.username + '：' + str(self.title)