# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('addman', '0004_address_address_set'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='is_validated',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='addressset',
            name='update_time',
            field=models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date updated'),
        ),
    ]
