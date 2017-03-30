from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    user = models.ForeignKey(User, unique=True)
    email = models.EmailField(blank=True)
    gender = models.CharField(max_length=2, choices=GENDER_CHOICES)
    phone = models.CharField(max_length=20, blank=True)
    qq_number = models.CharField(max_length=20, blank=True)
    birthday = models.DateField(blank=True)
    self_intro = models.CharField(max_length=200, blank=True)
    photo = models.ImageField(upload_to='accounts/', blank=True)

    def __str__(self):
        return 'User Profile for :' + self.user.username


