# Generated by Django 5.0.6 on 2024-07-01 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0031_rename_price_per_day_customuser_price_perday'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customuser',
            old_name='price_perday',
            new_name='price_per_day',
        ),
    ]
