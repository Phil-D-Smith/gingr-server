# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-13 21:20
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gingr_server', '0010_auto_20171113_2119'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userinfo',
            name='reg_date',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
