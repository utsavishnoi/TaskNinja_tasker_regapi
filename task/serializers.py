from rest_framework import serializers
from .models import Task

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['task_id', 'task_name', 'u_id', 't_id', 'task_desc']
        # Add 'read_only_fields' to prevent t_id from being required in POST requests
        read_only_fields = ['t_id']
