from django.db import models
from authe.models import CustomUser
from api.models import Tasker

class Task(models.Model):
    task_id = models.AutoField(primary_key=True)
    task_name = models.CharField(max_length=100)
    u_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    t_id = models.ForeignKey(Tasker, on_delete=models.CASCADE, null=True, blank=True)  # Allow null values
    task_desc = models.CharField(max_length=1000)


