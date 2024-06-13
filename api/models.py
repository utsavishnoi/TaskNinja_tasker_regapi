from django.conf import settings
from django.db import models

class Tasker(models.Model):
    tasker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=128)
    state = models.CharField(max_length=50, choices=settings.STATES_AND_UTS_CHOICES)
    city = models.CharField(max_length=50)
    about = models.TextField(blank=True)  # Optional field
    work = models.CharField(max_length=100, choices=settings.SERVICES_CHOICES)
    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class User(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=10)
    state = models.CharField(max_length=50, choices=settings.STATES_AND_UTS_CHOICES)
    city = models.CharField(max_length=50)
    work = models.CharField(max_length=100, choices=settings.SERVICES_CHOICES)
    added_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


