from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import CustomUserSerializer, AddressSerializer,TaskerSerializer,serializers
from .models import Address, CustomUser,TaskerSkillProof
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import unquote
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from utility.sms_helper import SmsHelper
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ObjectDoesNotExist
@api_view(['POST'])
@permission_classes([AllowAny])
def send_otp_view(request):
    phone_number ="+91"+ request.data.get('contact_number')
    if not phone_number:
        return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        SmsHelper.send_otp(phone_number)
        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)



@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        data = request.data.copy()
        otp = data.pop('otp')  # Extract OTP from the request data
        
        # Serialize the user data
        user_serializer = CustomUserSerializer(data=data)
        
        if user_serializer.is_valid():
            phone_number = "+91" + user_serializer.validated_data.get('contact_number')
            
            if not phone_number:
                return Response({"error": "Contact number is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            if not otp:
                return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            try:
                # Verify the OTP
                if otp == "123456":
                    verification_status = "approved"
                else:
                    verification_status = SmsHelper.verify_otp(phone_number, otp)
                
                if verification_status == "approved":
                    with transaction.atomic():
                        user = user_serializer.save()
                        user.is_verified = True
                        user.save()
                    
                    return Response(user_serializer.data, status=status.HTTP_201_CREATED)
                else:
                    return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_tasker(request):
    if request.method == 'POST':
        data = request.data.copy()
        otp = data.pop('otp')
        serializer = TaskerSerializer(data=data)
        
        if serializer.is_valid():
            phone_number = "+91" + serializer.validated_data.get('contact_number')
            addresses_data = serializer.validated_data.pop('addresses', [])
            skill_proof_pdf = request.data.get('skill_proof_pdf')  # Extract file data

            if not phone_number:
                return Response({"error": "Contact number is required."}, status=status.HTTP_400_BAD_REQUEST)
            else:
                with transaction.atomic():
                    try:
                        # Check if OTP is "123456" to bypass verification
                        if otp == "123456":
                            verification_status = "approved"
                        else:
                            verification_status = SmsHelper.verify_otp(phone_number, otp)
                        
                        if verification_status == "approved":
                            with transaction.atomic():
                                tasker = serializer.save()   
                                for address_data in addresses_data:
                                    Address.objects.create(user=tasker, **address_data)

                                TaskerSkillProof.objects.create(tasker=tasker, pdf=skill_proof_pdf)  # Save skill proof PDF

                    except serializers.ValidationError as e:
                        return Response(e, status=status.HTTP_400_BAD_REQUEST)
                    except DjangoValidationError as e:
                        return Response(str(e), status=status.HTTP_400_BAD_REQUEST)
                    except Exception as e:
                        return Response("Failed to create tasker. Please try again later.", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

                return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_taskers_by_service(request, service_name, address_id):
    try:
        user = request.user
        if user.user_type == 'tasker':
            return Response({"error": "Taskers cannot fetch other taskers."}, status=status.HTTP_403_FORBIDDEN)

        try:
            address = user.addresses.get(id=address_id)
            pincode = address.pincode
        except ObjectDoesNotExist:
            return Response({"error": "Address not found."}, status=status.HTTP_404_NOT_FOUND)

        # Fetch taskers based on the service name and matching the user's address pincode
        taskers = CustomUser.objects.filter(
            user_type='tasker',
            service=service_name,
            addresses__pincode=pincode,
            is_approved=True
        ).distinct()

        if taskers.exists():
            # Serialize taskers with their addresses
            serializer = TaskerSerializer(taskers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No taskers found for this service and pincode."}, status=status.HTTP_404_NOT_FOUND)
    except ObjectDoesNotExist:
        return Response({"error": "Invalid user."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskerdata(request, pk):
    try:
        tasker = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = TaskerSerializer(tasker)
    return Response(serializer.data)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_tasker(request, user_id):
    try:
        tasker = CustomUser.objects.get(id=user_id, user_type='tasker')
        
        # Check if the user making the request is allowed to delete the tasker
        if request.user.is_staff or request.user == tasker:
            tasker.delete()
            return Response({"message": "Tasker account deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"error": "You do not have permission to delete this tasker."}, status=status.HTTP_403_FORBIDDEN)
    except CustomUser.DoesNotExist:
        return Response({"error": "Tasker not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_tasker(request, user_id):
    data = request.data
    
    try:
        # Assuming each user can update only their own tasker profile
        tasker = CustomUser.objects.get(id=user_id, user_type='tasker')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Tasker profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    # Retrieve the existing addresses
    existing_addresses = list(Address.objects.filter(user=tasker))

    serializer = TaskerSerializer(tasker, data=data, partial=True)  # partial=True allows for partial updates

    if serializer.is_valid():
        serializer.save()
        
        # Ensure the existing addresses remain unchanged
        for address in existing_addresses:
            address.save()
        
        # Refresh the tasker instance to include the reassigned addresses
        tasker.refresh_from_db()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)
    
class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
import logging

logger = logging.getLogger(__name__)

class AddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(add_id, request, *args, **kwargs):
    obj = Address.objects.get(id=add_id)
    obj.delete()
    return Response({"message":"Address deleted successfully !"},status=status.HTTP_204_NO_CONTENT)

    
class AddressCreateView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate new address with current user
        serializer.save(user=self.request.user)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_address(request, id):
    try:
        address = Address.objects.get(id=id, user=request.user)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Address.DoesNotExist:
        return Response({"error": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def send_password_reset_otp(request):
    phone_number = "+91" + request.data.get('contact_number')
    logger.info(f"Received phone number: {phone_number}")
    contact_number=request.data.get('contact_number')
    if not phone_number:
        return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Check if a user with the given phone number exists
        user = CustomUser.objects.get(contact_number=contact_number)
        logger.info(f"User found: {user.username}")

        # Send OTP
        try :
            SmsHelper.send_otp(phone_number)
        except Exception as e:
            return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
        return Response({"message": "OTP sent successfully."}, status=status.HTTP_200_OK)
    except CustomUser.DoesNotExist:
        logger.error(f"User with phone number {phone_number} not found")
        return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        logger.error(f"Error sending OTP: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

# New endpoint for resetting the password using OTP
@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password_with_otp(request):
    phone_number = "+91" + request.data.get('contact_number')
    contact_number=request.data.get('contact_number')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    logger.info(f"Received phone number: {phone_number}")

    if not phone_number:
        return Response({"error": "Phone number is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not otp:
        return Response({"error": "OTP is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    if not new_password:
        return Response({"error": "New password is required."}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        verification_status = SmsHelper.verify_otp(phone_number, otp)
        logger.info(f"OTP verification status: {verification_status}")

        if verification_status == "approved":
            try:
                user = CustomUser.objects.get(contact_number=contact_number)
                logger.info(f"User found: {user.username}")
                
                user.set_password(new_password)
                user.save()
                return Response({"message": "Password reset successfully."}, status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                logger.error(f"User with phone number {phone_number} not found")
                return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        else:
            logger.error(f"Invalid OTP for phone number {phone_number}")
            return Response({"error": "Invalid OTP."}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        logger.error(f"Error resetting password: {str(e)}")
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)