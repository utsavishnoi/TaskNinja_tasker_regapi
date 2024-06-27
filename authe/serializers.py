from rest_framework import serializers
from .models import CustomUser,Address,TaskerSkillProof
from rest_framework.exceptions import ValidationError
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.db import transaction


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['id', 'name', 'state', 'city', 'pincode', 'full_address']

    def create(self, validated_data):
        user = self.context['request'].user  # Assuming you want to associate with the authenticated user
        address = Address.objects.create(user=user, **validated_data)
        return address

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.state = validated_data.get('state', instance.state)
        instance.city = validated_data.get('city', instance.city)
        instance.pincode = validated_data.get('pincode', instance.pincode)
        instance.full_address = validated_data.get('full_address', instance.full_address)
        instance.save()
        return instance
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

        #validated_data['password'] = make_password(validated_data['password'])

        with transaction.atomic():
            try:
                user = get_user_model().objects.create_user(**validated_data)

                for address_data in addresses_data:
                    Address.objects.create(user=user, **address_data)

            except serializers.ValidationError as e:
                logger.error(f"Validation error during user creation: {str(e)}")
                raise e

            except DjangoValidationError as e:
                logger.error(f"Django validation error during user creation: {str(e)}")
                raise serializers.ValidationError("Failed to create user. Please try again later.")

            except Exception as e:
                logger.error(f"Unexpected error during user creation: {str(e)}")
                raise serializers.ValidationError("Failed to create user. Please try again later.")

        return user

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses', [])

        instance.username = validated_data.get('username', instance.username)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.email = validated_data.get('email', instance.email)
        instance.contact_number = validated_data.get('contact_number', instance.contact_number)

        password = validated_data.get('password')
        if password:
            instance.set_password(password)

        instance.save()

        with transaction.atomic():
            try:
                existing_addresses = {address.id: address for address in instance.addresses.all()}
                for address_data in addresses_data:
                    address_id = address_data.get('id')
                    if address_id:
                        address = existing_addresses.pop(address_id, None)
                        if address:
                            # Update existing address
                            address_serializer = AddressSerializer(instance=address, data=address_data)
                            if address_serializer.is_valid():
                                address_serializer.save()
                            else:
                                raise serializers.ValidationError(address_serializer.errors)
                        else:
                            raise serializers.ValidationError(f"Address with id '{address_id}' does not exist for this user.")
                    else:
                        # Create new address
                        Address.objects.create(user=instance, **address_data)

                # Delete addresses not in addresses_data
                for address in existing_addresses.values():
                    address.delete()

            except serializers.ValidationError as e:
                logger.error(f"Validation error during user update: {str(e)}")
                raise e

            except Exception as e:
                logger.error(f"Unexpected error during user update: {str(e)}")
                raise serializers.ValidationError("Failed to update user. Please try again later.")

        return instance

class TaskerSerializer(serializers.ModelSerializer):
    addresses = AddressSerializer(many=True)
    skill_proof_pdf = serializers.FileField(required=True)  # Adjust this field as per your requirement

    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'password', 'service', 'experience',
                  'price', 'about', 'addresses', 'contact_number', 'skill_proof_pdf']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        addresses_data = validated_data.pop('addresses')
        skill_proof_pdf = validated_data.pop('skill_proof_pdf')

        validated_data['password'] = make_password(validated_data['password'])
        validated_data['user_type'] = 'tasker'

        # Create the tasker user
        tasker = CustomUser.objects.create(**validated_data)

        # Create addresses associated with the tasker
        for address_data in addresses_data:
            Address.objects.create(user=tasker, **address_data)

        # Create TaskerSkillProof for the tasker
        TaskerSkillProof.objects.create(tasker=tasker, pdf=skill_proof_pdf)

        return tasker

    def update(self, instance, validated_data):
        addresses_data = validated_data.pop('addresses')

        if 'password' in validated_data:
            instance.password = make_password(validated_data.pop('password'))

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update addresses associated with the tasker
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

class TaskerSkillProofSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskerSkillProof
        fields = ['id', 'tasker', 'pdf', 'uploaded_at']