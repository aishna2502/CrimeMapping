# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-16 15:19
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('crimeReporting', '0003_auto_20180316_2047'),
    ]

    operations = [
        migrations.AlterField(
            model_name='crime_timeline',
            name='TIME_OF_UPDATE',
            field=models.DateTimeField(blank=True, default=datetime.datetime(2018, 3, 16, 15, 19, 50, 265570, tzinfo=utc)),
        ),
    ]
