# models.py

from django.db import models
from request.models import Request
from authe.models import CustomUser

class Notification(models.Model):
    STATUS_CHOICE = [
        (0, "unread"),
        (1, "read")
    ]

    notification_id = models.AutoField(primary_key=True)
    request = models.ForeignKey(Request, on_delete=models.CASCADE)
    message = models.CharField(max_length=100)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    status = models.IntegerField(choices=STATUS_CHOICE, default=0)
    created_at = models.DateTimeField(auto_now_add=True) 
