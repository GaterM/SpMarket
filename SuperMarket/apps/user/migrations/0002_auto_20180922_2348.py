# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-22 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('province', models.CharField(max_length=20)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='reg_login',
            name='address',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='详细地址'),
        ),
        migrations.AlterField(
            model_name='reg_login',
            name='sex',
            field=models.SmallIntegerField(choices=[(1, '男'), (2, '女'), (3, '保密')], default=3, verbose_name='性别'),
        ),
    ]