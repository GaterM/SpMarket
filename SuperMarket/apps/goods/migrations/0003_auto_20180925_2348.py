# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2018-09-25 15:48
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('goods', '0002_auto_20180925_1919'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='activity_goods',
            options={'verbose_name': '首页活动商品', 'verbose_name_plural': '首页活动商品'},
        ),
        migrations.AlterField(
            model_name='activity_area',
            name='name',
            field=models.CharField(max_length=50, verbose_name='专区名称'),
        ),
        migrations.AlterModelTable(
            name='activity_goods',
            table='Activity_goods',
        ),
    ]