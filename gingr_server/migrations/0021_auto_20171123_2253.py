# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-23 22:53
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gingr_server', '0020_auto_20171114_2048'),
    ]

    operations = [
        migrations.RenameField(
            model_name='match',
            old_name='match_id',
            new_name='match',
        ),
    ]