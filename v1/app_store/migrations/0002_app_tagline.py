# Generated by Django 3.1.1 on 2021-08-31 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_store', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='app',
            name='tagline',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]