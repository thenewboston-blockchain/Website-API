# Generated by Django 3.1.1 on 2020-10-12 01:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contributors', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='contributor',
            name='account_number',
            field=models.CharField(default=123, max_length=64),
            preserve_default=False,
        ),
    ]