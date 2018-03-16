# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2018-03-16 15:13
from __future__ import unicode_literals

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
from django.utils.timezone import utc


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0008_alter_user_username_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='CRIME_TIMELINE',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('CURRENT_STATUS', models.CharField(choices=[('lodged', 'LODGED'), ('pending', 'PENDING'), ('investigated', 'INVESTIGATED'), ('evidence_collection', 'EVIDENCE COLLECTION'), ('moved', 'MOVED TO COURT'), ('closed', 'CLOSED')], default='Pending', max_length=100)),
                ('TIME_OF_UPDATE', models.DateTimeField(blank=True, default=datetime.datetime(2018, 3, 16, 15, 13, 3, 758182, tzinfo=utc))),
                ('DESCRIPTION', models.CharField(blank=True, default='Pending', max_length=1000, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='FIR_REPORT',
            fields=[
                ('ID', models.AutoField(primary_key=True, serialize=False)),
                ('CRIME_TYPE', models.CharField(max_length=100)),
                ('LAT', models.FloatField()),
                ('LNG', models.FloatField()),
                ('CRIME_DESCRIPTION', models.CharField(blank=True, max_length=1000, null=True)),
                ('COMPLAINT_BY', models.CharField(max_length=100)),
                ('DATE_CRIME', models.DateField(blank=True, verbose_name='Conversation Date')),
                ('TIME_CRIME', models.TimeField(blank=True, verbose_name='Conversation Time')),
                ('FIR_LOC', models.CharField(max_length=100)),
                ('COMPLAINT_TIME', models.TimeField(blank=True, verbose_name='Conversation Time')),
                ('PHONE', models.CharField(max_length=100)),
                ('STATUS', models.CharField(choices=[('lodged', 'LODGED'), ('pending', 'PENDING'), ('investigated', 'INVESTIGATED'), ('evidence_collection', 'EVIDENCE COLLECTION'), ('moved', 'MOVED TO COURT'), ('closed', 'CLOSED')], default='Lodged', max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='USER',
            fields=[
                ('USER_REF', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='USER', serialize=False, to=settings.AUTH_USER_MODEL)),
                ('NAME', models.CharField(max_length=100)),
                ('PASSWORD', models.CharField(max_length=6)),
            ],
        ),
        migrations.AddField(
            model_name='fir_report',
            name='PERSON_COMPLAINT',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.USER'),
        ),
        migrations.AddField(
            model_name='crime_timeline',
            name='CRIME_ID',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.FIR_REPORT'),
        ),
        migrations.AddField(
            model_name='crime_timeline',
            name='UPDATED_BY',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='crimeReporting.USER'),
        ),
    ]
