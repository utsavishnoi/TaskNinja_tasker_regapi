from rest_framework import serializers
from .models import Tasker

class TaskerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasker
        fields = ['name', 'email', 'password', 'state', 'city', 'about', 'service']
        extra_kwargs = {
            'password': {'write_only': True}
        }

