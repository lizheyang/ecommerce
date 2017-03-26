# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0003_auto_20170325_2316'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='subtitle',
            field=models.CharField(blank=True, max_length=200),
        ),
    ]
