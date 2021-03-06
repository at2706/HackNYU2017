# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-18 20:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('HackNYU', '0013_auto_20170218_1236'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='labreport',
            name='user',
        ),
        migrations.AddField(
            model_name='labreport',
            name='doctor',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='lab', to='HackNYU.Doctor'),
        ),
        migrations.AlterField(
            model_name='labreport',
            name='patient',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='lab', to='HackNYU.Patient'),
        ),
    ]
