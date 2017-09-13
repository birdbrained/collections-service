# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-09-13 15:18
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Parameter',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('value', django.contrib.postgres.fields.jsonb.JSONField()),
                ('properties', django.contrib.postgres.fields.jsonb.JSONField()),
                ('case', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='workflow.Case')),
            ],
        ),
        migrations.CreateModel(
            name='Section',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Widget',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('label', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('widget_type', models.CharField(max_length=24)),
            ],
        ),
        migrations.CreateModel(
            name='WidgetParameterMapping',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=64)),
                ('parameter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='widget_parameter_mappings', to='workflow.Parameter')),
            ],
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=128)),
                ('description', models.TextField(blank=True)),
                ('initialization_values', django.contrib.postgres.fields.jsonb.JSONField()),
            ],
        ),
        migrations.AddField(
            model_name='widgetparametermapping',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widget_parameter_mappings', to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='widget',
            name='parameter_mappings',
            field=models.ManyToManyField(related_name='consumer_widgets', to='workflow.WidgetParameterMapping'),
        ),
        migrations.AddField(
            model_name='widget',
            name='section',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widgets', to='workflow.Section'),
        ),
        migrations.AddField(
            model_name='widget',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='widgets', to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='section',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='parameter',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parameters', to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='case',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cases', to='workflow.Workflow'),
        ),
        migrations.AlterUniqueTogether(
            name='parameter',
            unique_together=set([('case', 'name')]),
        ),
    ]
