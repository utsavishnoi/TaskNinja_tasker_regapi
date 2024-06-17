from rest_framework import serializers
from .models import Tasker, Address
from rest_framework.exceptions import ValidationError

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['name', 'state', 'city', 'full_address']

    def create(self, validated_data):
        tasker = self.context['tasker']
        validated_data['tasker'] = tasker
        return super().create(validated_data)

class TaskerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)

    class Meta:
        model = Tasker
        fields = ['name', 'email', 'password', 'about', 'service', 'addresses']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        tasker = Tasker.objects.create(**validated_data)
        
        for address_data in addresses_data:
            
            if Address.objects.filter(tasker=tasker, name=address_data['name']).exists():
                raise ValidationError(f"Address with name '{address_data['name']}' already exists for this tasker.")
            
            Address.objects.create(tasker=tasker, **address_data)
        
        return tasker
