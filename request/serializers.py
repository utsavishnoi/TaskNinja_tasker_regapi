from rest_framework import serializers
from .models import Request
from authe.models import CustomUser

class RequestSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())
    tasker = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all())

    class Meta:
        model = Request
        fields = ['req_id', 'user', 'tasker', 'service_desc', 'status','booking_date','service_date']