from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')

class Address(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='addresses', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=50, choices=settings.STATES_AND_UTS_CHOICES)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    full_address = models.TextField()

    class Meta:
        unique_together = ('user', 'name')

    def __str__(self):
        return f"{self.name} - {self.user.username}"
