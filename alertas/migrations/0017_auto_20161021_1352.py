# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-10-21 13:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('alertas', '0016_auto_20161021_1234'),
    ]

    operations = [
        migrations.AlterField(
            model_name='threat',
            name='name',
            field=models.CharField(max_length=100),
        ),
    ]
