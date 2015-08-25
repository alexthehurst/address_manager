# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('addman', '0003_addressset'),
    ]

    operations = [
        migrations.AddField(
            model_name='address',
            name='address_set',
            field=models.ForeignKey(default=1, to='addman.AddressSet'),
            preserve_default=False,
        ),
    ]
