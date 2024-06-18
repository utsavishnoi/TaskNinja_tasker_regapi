from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.auth import get_user_model

class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')


User = get_user_model()

class Address(models.Model):
    user = models.ForeignKey(User, related_name='addresses', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    full_address = models.TextField()

    def __str__(self):
        return f"{self.name}, {self.city}, {self.state}, {self.pincode}"

    class Meta:
        unique_together = ('user', 'name')  # Ensures name is unique per tasker

