# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-11-06 19:32
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0002_workflow_case_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workflow',
            options={'permissions': [('read', 'read'), ('execute', 'execute')]},
        ),
    ]
