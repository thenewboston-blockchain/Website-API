# Generated by Django 3.1.6 on 2021-03-24 06:20

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('videos', '0003_auto_20210211_0627'),
    ]

    operations = [
        migrations.AddField(
            model_name='playlist',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250), default=[], size=None),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='video',
            name='category',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=250, null=True), blank=True, default=list, size=None),
        ),
    ]