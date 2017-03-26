# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0004_product_subtitle'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='thumb',
            field=models.ImageField(upload_to='catalog/thumb/', blank=True),
        ),
    ]
