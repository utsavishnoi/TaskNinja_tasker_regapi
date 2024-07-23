# Generated by Django 5.0.6 on 2024-07-23 06:26

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('request', '0007_remove_address_task_address_request'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('notification_id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.CharField(max_length=100)),
                ('status', models.IntegerField(choices=[(0, 'unread'), (1, 'read')], default=0)),
                ('request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='request.request')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
