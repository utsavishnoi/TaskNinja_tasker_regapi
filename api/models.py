from django.db import models

class Company(models.Model):
    company_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=50)
    about = models.TextField()
    phone=models.CharField(max_length=10)
    email=models.EmailField(max_length=100)
    work = models.CharField(
        max_length=100,
        choices=[
            ('Plumber', 'Plumber'),
            ('Packers and Movers', 'Packers and Movers'),
            ('Electrician', 'Electrician'),
            ('Cleaning Services', 'Cleaning Services'),
            ('Carpenters', 'Carpenters'),
            ('Pest Control', 'Pest Control'),
            ('Painters', 'Painters'),
            ('AC Services', 'AC Services'),
            ('Gardening', 'Gardening'),
            ('Home Security', 'Home Security'),
            ('Laundry', 'Laundry'),
            ('Moving Services', 'Moving Services'),
            ('Home Cleaning', 'Home Cleaning'),
            ('Furniture Assembly', 'Furniture Assembly'),
            ('Computer Repair', 'Computer Repair'),
            ('Interior Design', 'Interior Design'),
        ]
    )
    added_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return self.name+'--'+ self.location


class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    address = models.CharField(max_length=500)
    phone = models.CharField(max_length=10)
    location = models.CharField(max_length=50)
    work = models.CharField(
        max_length=100,
        choices=[
            ('Plumber', 'Plumber'),
            ('Packers and Movers', 'Packers and Movers'),
            ('Electrician', 'Electrician'),
            ('Cleaning Services', 'Cleaning Services'),
            ('Carpenters', 'Carpenters'),
            ('Pest Control', 'Pest Control'),
            ('Painters', 'Painters'),
            ('AC Services', 'AC Services'),
            ('Gardening', 'Gardening'),
            ('Home Security', 'Home Security'),
            ('Laundry', 'Laundry'),
            ('Moving Services', 'Moving Services'),
            ('Home Cleaning', 'Home Cleaning'),
            ('Furniture Assembly', 'Furniture Assembly'),
            ('Computer Repair', 'Computer Repair'),
            ('Interior Design', 'Interior Design'),
        ]
    )
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    def __str__(self):
        return self.name 

