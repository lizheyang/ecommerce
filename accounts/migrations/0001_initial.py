# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', auto_created=True, primary_key=True)),
                ('gender', models.CharField(max_length=2, choices=[('M', 'Male'), ('F', 'Female')])),
                ('phone', models.CharField(max_length=20)),
                ('qq_number', models.CharField(max_length=20, blank=True)),
                ('birthday', models.DateField(blank=True)),
                ('self_intro', models.CharField(max_length=200, blank=True)),
                ('photo', models.ImageField(blank=True, upload_to='accounts/')),
                ('user', models.ForeignKey(unique=True, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
