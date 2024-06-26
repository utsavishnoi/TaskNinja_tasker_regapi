from rest_framework import serializers
from .models import CustomUser,Address
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id','name', 'state', 'city', 'full_address','pincode']

    def create(self, validated_data):
        user = self.context['user']
        validated_data['user'] = user
        return super().create(validated_data)

class CustomUserSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True) 
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'contact_number', 'addresses']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['user_type'] = 'user'
        user = CustomUser.objects.create(**validated_data)
        for address_data in addresses_data:

            if Address.objects.filter(user=user, name=address_data['name']).exists():
                raise ValidationError(f"Address with name '{address_data['name']}' already exists for this tasker.")

            Address.objects.create(user=user, **address_data)

        return user

class TaskerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    class Meta:
        model = CustomUser
        fields = ['id','username','first_name','last_name','email','password','service','price','about','addresses','contact_number','addresses']
        extra_kwargs = {'password' : {'write_only': True}}
        
    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        validated_data['password'] = make_password(validated_data['password'])
        validated_data['user_type'] = 'tasker'
        user = CustomUser.objects.create(**validated_data)

        for address_data in addresses_data:

            if Address.objects.filter(user=user, name=address_data['name']).exists():
                raise ValidationError(f"Address with name '{address_data['name']}' already exists for this tasker.")

            Address.objects.create(user=user, **address_data)

        return user
    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', None)
        
        if 'password' in validated_data:
            instance.password = make_password(validated_data.pop('password'))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if addresses_data is not None:
            for address_data in addresses_data:
                address_instance, created = Address.objects.get_or_create(
                    user=instance,
                    id=address_data.get('id'),
                    defaults=address_data
                )
                if not created:
                    for attr, value in address_data.items():
                        setattr(address_instance, attr, value)
                    address_instance.save()

        return instance