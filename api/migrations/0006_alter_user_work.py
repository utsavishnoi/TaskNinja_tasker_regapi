# Generated by Django 5.0.6 on 2024-06-10 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_user_work'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='work',
            field=models.CharField(choices=[('Plumber', 'Plumber'), ('Packers and Movers', 'Packers and Movers'), ('Electrician', 'Electrician'), ('Cleaning Services', 'Cleaning Services'), ('Carpenters', 'Carpenters'), ('Pest Control', 'Pest Control'), ('Painters', 'Painters'), ('AC Services', 'AC Services'), ('Gardening', 'Gardening'), ('Home Security', 'Home Security'), ('Laundry', 'Laundry'), ('Moving Services', 'Moving Services'), ('Home Cleaning', 'Home Cleaning'), ('Furniture Assembly', 'Furniture Assembly'), ('Computer Repair', 'Computer Repair'), ('Interior Design', 'Interior Design')], max_length=100),
        ),
    ]
