from rest_framework import serializers
from .models import Tasker

from rest_framework import serializers
from .models import Tasker

class TaskerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tasker
        fields = '__all__'



