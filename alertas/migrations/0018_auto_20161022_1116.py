# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-22 11:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0017_auto_20161021_1352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threat',
            name='scientific_name',
            field=models.CharField(max_length=100),
        ),
    ]
