# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-09-30 11:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0011_auto_20160830_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='detection',
            name='location_lat',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='detection',
            name='location_long',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
    ]
