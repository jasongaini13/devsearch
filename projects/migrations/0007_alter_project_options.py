# Generated by Django 5.0.3 on 2024-04-13 05:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_alter_project_options_review_owner'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-Vote_ratio', '-Vote_total', 'title']},
        ),
    ]