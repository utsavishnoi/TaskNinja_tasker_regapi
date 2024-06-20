# Generated by Django 5.0.6 on 2024-06-20 07:15

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Tasker',
            fields=[
                ('tasker_id', models.AutoField(primary_key=True, serialize=False)),
                ('username', models.CharField(max_length=50, unique=True)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('password', models.CharField(max_length=100)),
                ('about', models.CharField(max_length=100)),
                ('is_active', models.BooleanField(default=True)),
                ('service', models.CharField(max_length=100)),
                ('address_city', models.CharField(max_length=100)),
                ('address_full', models.CharField(max_length=500)),
                ('pincode', models.CharField(max_length=6)),
            ],
        ),
    ]
