# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-14 00:18
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('workflow', '0003_widgetparametermapping_case'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='widget',
            name='parameter_mappings',
        ),
        migrations.AddField(
            model_name='widgetparametermapping',
            name='widget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='widget_parameter_mappings', to='workflow.Widget'),
        ),
    ]