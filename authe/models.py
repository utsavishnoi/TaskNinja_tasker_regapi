from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        (1, 'user'),
        (2, 'tasker'),
    ]

    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='user')
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    about = models.CharField(max_length=100, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    service = models.CharField(max_length=100, blank=True, null=True)
    price = models.DecimalField(max_digits=5, decimal_places=1, blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=5,decimal_places=2,blank=True,null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

    def __str__(self):
        return self.username

class Address(models.Model):
    user = models.ForeignKey(CustomUser, related_name='addresses', db_column='user_id', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    full_address = models.CharField(max_length=500)
    pincode = models.CharField(max_length=6)

    class Meta:
        unique_together = ('user', 'name')  # Ensures name is unique per user

    def __str__(self):
        return self.name
