from django.db import models
from authe.models import CustomUser

# Create your models here.
class Request(models.Model):  # Inherit from models.Model
    STATUS_CHOICE = [
        (1, 'Requested'),
        (2, 'Booked'),
        (3, 'Cancelled'),
        (4, 'Rejected')
    ]
    
    req_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, db_column='user_id', on_delete=models.CASCADE, related_name='requests')
    tasker = models.ForeignKey(CustomUser, db_column='tasker_id', on_delete=models.CASCADE, related_name='tasks')
    service_desc = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICE)  # Use IntegerField for status choices
    service_date = models.DateTimeField()
    booking_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request {self.req_id} by {self.user.username} for {self.tasker.username}"
