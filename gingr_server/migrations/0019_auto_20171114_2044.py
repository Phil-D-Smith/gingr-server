# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 20:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gingr_server', '0018_auto_20171114_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='dob',
            field=models.DateField(default=None),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='photo',
            field=models.ImageField(default=None, upload_to='profile-photos/%s'),
        ),
    ]
