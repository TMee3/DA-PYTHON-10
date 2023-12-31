# Generated by Django 4.2.5 on 2023-09-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("API_IssueTrackingSystem", "0006_alter_contributor_unique_together"),
    ]

    operations = [
        migrations.RenameField(
            model_name="issue",
            old_name="user",
            new_name="assigned_to",
        ),
        migrations.AddField(
            model_name="comment",
            name="updated_time",
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name="issue",
            name="updated_time",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
