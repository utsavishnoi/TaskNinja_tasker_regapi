# Generated by Django 5.0.6 on 2024-07-01 06:13

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authe', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='experience',
            field=models.CharField(blank=True, choices=[('Less than 1 year', 'Less than 1 year'), ('1-2 years', '1-2 years'), ('2-3 years', '2-3 years'), ('More than 3 years', 'More than 3 years')], max_length=20, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='customuser',
            name='skill_proof_pdf',
            field=models.CharField(blank=True, max_length=1024, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='full_address',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='address',
            name='state',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='address',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='price',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.CreateModel(
            name='TaskerSkillProof',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pdf', models.CharField(blank=True, max_length=1024)),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('tasker', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='skill_proofs', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
