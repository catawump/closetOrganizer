# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-22 15:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mycloset', '0003_remove_clothes_last_worn'),
    ]

    operations = [
        migrations.AddField(
            model_name='clothes',
            name='description',
            field=models.CharField(default='It is clothes.', max_length=255),
            preserve_default=False,
        ),
    ]