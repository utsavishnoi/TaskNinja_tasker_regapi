from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Address
from django.db import transaction
from django.contrib.auth.hashers import make_password

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'state', 'city', 'pincode', 'full_address']

class CustomUserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True, required=False)

    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'first_name', 'last_name', 'email', 'password', 'contact_number', 'addresses')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses', [])
        
        # Hash the password
        validated_data['password'] = make_password(validated_data['password'])
        
        with transaction.atomic():
            user = get_user_model().objects.create_user(**validated_data)

            for address_data in addresses_data:
                if Address.objects.filter(user=user, name=address_data['name']).exists():
                    raise serializers.ValidationError(f"Address with name '{address_data['name']}' already exists for this user.")
                
                Address.objects.create(user=user, **address_data)

        return user

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])

        # Update user fields
        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)

        # Update password if provided
        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        # Save the updated user instance
        instance.save()

        with transaction.atomic():
            # Update addresses
            existing_addresses = {address.id: address for address in instance.addresses.all()}
            for address_data in addresses_data:
                address_id = address_data.get('id')
                if address_id:
                    address = existing_addresses.pop(address_id, None)
                    if address:
                        address.name = address_data.get('name', address.name)
                        address.state = address_data.get('state', address.state)
                        address.city = address_data.get('city', address.city)
                        address.pincode = address_data.get('pincode', address.pincode)
                        address.full_address = address_data.get('full_address', address.full_address)
                        address.save()
                    else:
                        raise serializers.ValidationError(f"Address with id '{address_id}' does not exist for this user.")
                else:
                    Address.objects.create(user=instance, **address_data)

            # Delete remaining addresses
            for address in existing_addresses.values():
                address.delete()

        return instance
