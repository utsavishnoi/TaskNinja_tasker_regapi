from django.db import models

class Tasker(models.Model):
    tasker_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    service = models.CharField(max_length=100)
    about = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    price_per_hour = models.CharField(max_length=5, blank=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    tasker = models.ForeignKey(Tasker, related_name='addresses', db_column='tasker_id_id', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    state = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100)
    full_address = models.CharField(max_length=500)

    class Meta:
        unique_together = ('tasker', 'name')  # Ensures name is unique per tasker

    def __str__(self):
        return self.name
