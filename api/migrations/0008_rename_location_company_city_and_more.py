# Generated by Django 5.0.6 on 2024-06-10 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_company_email_company_phone'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='location',
            new_name='city',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='location',
            new_name='city',
        ),
        migrations.RemoveField(
            model_name='company',
            name='email',
        ),
        migrations.RemoveField(
            model_name='company',
            name='phone',
        ),
        migrations.AddField(
            model_name='company',
            name='state',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(default=1, max_length=50),
            preserve_default=False,
        ),
    ]
