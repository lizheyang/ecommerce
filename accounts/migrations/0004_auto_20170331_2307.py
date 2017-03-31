# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_auto_20170331_2301'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birthday',
            field=models.DateField(null=True, blank=True, verbose_name='生日'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='email',
            field=models.EmailField(max_length=254, blank=True, verbose_name='电子邮箱'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='gender',
            field=models.CharField(max_length=2, choices=[('M', '男'), ('F', '女')], verbose_name='性别'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(max_length=20, blank=True, verbose_name='手机号码'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(upload_to='accounts/', blank=True, verbose_name='头像'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='qq_number',
            field=models.CharField(max_length=20, blank=True, verbose_name='QQ号码'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='self_intro',
            field=models.TextField(blank=True, verbose_name='自我介绍'),
        ),
    ]
