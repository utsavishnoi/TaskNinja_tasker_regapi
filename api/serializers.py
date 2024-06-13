from rest_framework import serializers
from .models import Tasker, User

class TaskerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasker
        fields = ['tasker_id', 'name', 'state', 'city', 'email', 'password', 'about', 'work', 'added_date']
        extra_kwargs = {
            'password': {'write_only': True}
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'phone', 'state', 'city']

from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
