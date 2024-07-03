from rest_framework import serializers
from .models import Request

class RequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = Request
        fields = ['req_id', 'user', 'tasker', 'service_desc', 'status', 'booking_date', 'service_date']
