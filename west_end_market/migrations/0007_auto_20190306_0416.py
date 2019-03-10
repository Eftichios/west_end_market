# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-03-06 04:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('west_end_market', '0006_auto_20190304_2336'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(blank=True, max_length=250),
        ),
        migrations.AlterField(
            model_name='listing',
            name='picture',
            field=models.ImageField(upload_to='photos/'),
        ),
    ]