# Generated by Django 3.1.1 on 2020-10-10 22:32

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
        ('contributors', '0001_initial'),
        ('meta', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Opening',
            fields=[
                ('created_date', models.DateTimeField(auto_now_add=True, db_index=True, null=True)),
                ('modified_date', models.DateTimeField(auto_now=True, db_index=True)),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('active', models.BooleanField(db_index=True, default=True)),
                ('description', models.TextField()),
                ('eligible_for_task_points', models.BooleanField(db_index=True, default=False)),
                ('pay_per_day', models.PositiveIntegerField()),
                ('title', models.CharField(max_length=250)),
                ('reports_to', models.ManyToManyField(to='contributors.Contributor')),
                ('responsibilities', models.ManyToManyField(to='meta.Responsibility')),
                ('skills', models.ManyToManyField(to='meta.Skill')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teams.team')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
