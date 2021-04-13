# Generated by Django 3.1.6 on 2021-03-24 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0012_auto_20210313_1912'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='coremember',
            name='pay_per_day',
        ),
        migrations.AddField(
            model_name='coremember',
            name='hourly_rate',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='coremember',
            name='weekly_hourly_commitment',
            field=models.PositiveIntegerField(default=0),
        ),
    ]