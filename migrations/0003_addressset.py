# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('addman', '0002_auto_20150819_0312'),
    ]

    operations = [
        migrations.CreateModel(
            name='AddressSet',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('set_name', models.CharField(max_length=150)),
                ('set_description', models.CharField(max_length=1000, blank=True)),
                ('creation_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('update_time', models.DateTimeField(default=django.utils.timezone.now, verbose_name=b'date created')),
                ('owner', models.CharField(max_length=30)),
            ],
        ),
    ]
