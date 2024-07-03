from rest_framework import serializers
from .models import Request, Address

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['state', 'city', 'pincode', 'full_address']

class RequestSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = Request
        fields = ['req_id','user', 'tasker', 'service_desc', 'status', 'booking_date', 'service_date', 'address']

    def create(self, validated_data):
        address_data = validated_data.pop('address')
        request = Request.objects.create(**validated_data)
        Address.objects.create(request=request, **address_data)
        return request
