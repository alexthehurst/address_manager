# -*- coding: utf-8 -*-
# Generated by Django 1.9.3 on 2016-03-04 07:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('addman', '0007_auto_20160303_0709'),
    ]

    operations = [
        migrations.RenameField(
            model_name='address',
            old_name='zip',
            new_name='zip5',
        ),
        migrations.AddField(
            model_name='address',
            name='zip4',
            field=models.CharField(blank=True, max_length=4),
        ),
        migrations.AlterField(
            model_name='address',
            name='status',
            field=models.CharField(choices=[(b'UNSUBMITTED', b'Not yet processed'), (b'FAILED', b'No match found'), (b'MATCHED_PARTIAL', b'Tentative match, confirmation required'), (b'MATCHED', b'Validated and deliverable')], default=b'UNSUBMITTED', max_length=50),
        ),
    ]