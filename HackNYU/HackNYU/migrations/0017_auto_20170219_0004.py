# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-19 05:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('HackNYU', '0016_auto_20170218_1626'),
    ]

    operations = [
        migrations.AddField(
            model_name='hospitaladdress',
            name='lat',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=22),
        ),
        migrations.AddField(
            model_name='hospitaladdress',
            name='lng',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=22),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='lat',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=22),
        ),
        migrations.AddField(
            model_name='useraddress',
            name='lng',
            field=models.DecimalField(decimal_places=16, default=0, max_digits=22),
        ),
    ]