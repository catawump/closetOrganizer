# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-23 16:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycloset', '0005_outfit'),
    ]

    operations = [
        migrations.AddField(
            model_name='outfit',
            name='outfit_creator',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='user_outfits', to='mycloset.User'),
            preserve_default=False,
        ),
    ]