# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 21:15
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gingr_server', '0002_auto_20171113_2115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='reg_date',
            field=models.DateTimeField(default=datetime.datetime(2017, 11, 13, 21, 15, 40, 619220)),
        ),
    ]
