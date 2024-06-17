from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.conf import settings

class CustomUser(AbstractUser):
    contact_number = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=50, choices=settings.STATES_AND_UTS_CHOICES)
    city = models.CharField(max_length=100, blank=True, null=True)
    pincode = models.CharField(max_length=6, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    groups = models.ManyToManyField(Group, related_name='custom_user_groups')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions')
