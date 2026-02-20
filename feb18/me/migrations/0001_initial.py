# Generated manually for initial portfolio schema.
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Experience',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=120)),
                ('role', models.CharField(max_length=120)),
                ('period', models.CharField(max_length=80)),
                ('summary', models.TextField()),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['sort_order', 'company'],
            },
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(max_length=120)),
                ('role', models.CharField(max_length=120)),
                ('tagline', models.CharField(max_length=180)),
                ('bio', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('location', models.CharField(max_length=120)),
                ('github_url', models.URLField(blank=True)),
                ('linkedin_url', models.URLField(blank=True)),
                ('resume_url', models.URLField(blank=True)),
            ],
            options={
                'verbose_name': 'Profile',
                'verbose_name_plural': 'Profile',
            },
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('description', models.TextField()),
                ('tech_stack', models.CharField(max_length=200)),
                ('project_url', models.URLField(blank=True)),
                ('repo_url', models.URLField(blank=True)),
                ('featured', models.BooleanField(default=True)),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['sort_order', '-featured', 'title'],
            },
        ),
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=80)),
                ('name', models.CharField(max_length=80)),
                ('level', models.PositiveSmallIntegerField(default=80)),
                ('sort_order', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'ordering': ['sort_order', 'category', 'name'],
            },
        ),
    ]
