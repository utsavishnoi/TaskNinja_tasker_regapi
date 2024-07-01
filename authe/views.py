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

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        data = request.data.copy()
        
        # Serialize the user data
        user_serializer = CustomUserSerializer(data=data)
        
        # Validate and save user data
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def register_tasker(request):
    if request.method == 'POST':
        serializer = TaskerSerializer(data=request.data)
        
        if serializer.is_valid():
            addresses_data = serializer.validated_data.pop('addresses', [])
            skill_proof_pdf = request.data.get('skill_proof_pdf')  # Extract file data

            with transaction.atomic():
                try:
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
def list_taskers_by_service(request, service_name):
    try:
        user = request.user
        if user.user_type == 'tasker':
            return Response({"error": "Taskers cannot fetch other taskers."}, status=status.HTTP_403_FORBIDDEN)

        # Get all pincodes associated with the user's addresses
        pincodes = user.addresses.values_list('pincode', flat=True)

        # Fetch taskers based on the service name and matching any of the user's pincodes
        taskers = CustomUser.objects.filter(
            user_type='tasker',
            service=service_name,
            addresses__pincode__in=pincodes
        ).distinct()

        if taskers.exists():
            # Serialize taskers with their addresses
            serializer = TaskerSerializer(taskers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No taskers found for this service and pincode."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def taskerdata(request, pk):
    try:
        tasker = CustomUser.objects.get(pk=pk)
    except CustomUser.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = TaskerSerializer(tasker)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = TaskerSerializer(tasker, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        tasker.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
        tasker = CustomUser.objects.get(id=user_id,user_type = 'tasker')
    except CustomUser.DoesNotExist:
        return Response({'error': 'Tasker profile not found.'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = TaskerSerializer(tasker, data=data, partial=True)  # partial=True allows for partial updates

    if serializer.is_valid():
        serializer.save()
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
    return Response(status=status.HTTP_204_NO_CONTENT)

    
class AddressCreateView(generics.CreateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Automatically associate new address with current user
        serializer.save(user=self.request.user)

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_user(request, id):
    try:
        address = Address.objects.get(id=id, user=request.user)
        address.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except Address.DoesNotExist:
        return Response({"error": "Address not found."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    