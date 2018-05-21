# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-21 19:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mycloset', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='item_creator',
            field=models.ForeignKey(default=0, on_delete=django.db.models.deletion.CASCADE, related_name='user_clothes', to='mycloset.User'),
            preserve_default=False,
        ),
    ]
