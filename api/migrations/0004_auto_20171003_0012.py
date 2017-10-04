# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-10-03 00:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_auto_20171003_0010'),
    ]

    operations = [
        migrations.AlterField(
            model_name='collection',
            name='workflow',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='collections', to='workflow.Workflow'),
        ),
    ]