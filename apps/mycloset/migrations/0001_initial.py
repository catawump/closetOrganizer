# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-05-21 16:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Clothes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mainType', models.CharField(max_length=255)),
                ('subType', models.CharField(max_length=255)),
                ('color', models.CharField(max_length=255)),
                ('weather', models.CharField(max_length=255)),
                ('fanciness', models.CharField(max_length=255)),
                ('clean', models.BooleanField()),
                ('favorite', models.BooleanField()),
                ('pattern', models.CharField(max_length=255)),
                ('last_worn', models.DateField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('email', models.CharField(max_length=255)),
                ('password', models.CharField(max_length=255)),
            ],
        ),
    ]
