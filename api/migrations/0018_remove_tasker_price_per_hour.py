# Generated by Django 5.0.6 on 2024-06-12 06:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0017_rename_is_active_tasker_active_remove_tasker_id_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasker',
            name='price_per_hour',
        ),
    ]
