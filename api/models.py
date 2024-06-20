# api/models.py

from django.db import models

class Tasker(models.Model):
    tasker_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)  # You should handle password hashing separately
    about = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    service = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=5,decimal_places=1)
    address_state = models.CharField(max_length=50)
    address_city = models.CharField(max_length=100)
    address_full = models.CharField(max_length=500)
    pincode = models.CharField(max_length=6)
    is_verified = models.BooleanField(default=False)
    phone_no = models.CharField(max_length=10)
    def __str__(self):
        return self.username
