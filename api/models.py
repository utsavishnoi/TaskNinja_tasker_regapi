# models.py

from django.db import models

class Tasker(models.Model):
    tasker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    about = models.CharField(max_length=100)

    def __str__(self):
        return self.name
