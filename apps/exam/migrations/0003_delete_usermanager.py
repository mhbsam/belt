# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-27 16:38
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0002_usermanager'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserManager',
        ),
    ]
