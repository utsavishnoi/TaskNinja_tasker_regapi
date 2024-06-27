from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import CustomUserSerializer, AddressSerializer,TaskerSerializer
from .models import Address, CustomUser
from rest_framework.views import APIView
from rest_framework.response import Response
from urllib.parse import unquote


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
        print(request.data)  # Output request data to console for debugging
        data = request.data.copy()

        # Extract skill proof PDF from request data
        skill_proof_pdf = request.FILES.get('skill_proof_pdf')

        # Add skill_proof_pdf to data dict
        data['skill_proof_pdf'] = skill_proof_pdf

        tasker_serializer = TaskerSerializer(data=data)

        if tasker_serializer.is_valid():
            tasker = tasker_serializer.save()
            return Response(tasker_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(tasker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_taskers_by_service(request, service_name):
    try:
        service_name = unquote(service_name)
        # Fetch taskers based on the service name
        taskers = CustomUser.objects.filter(user_type='tasker', service=service_name)
        
        if taskers.exists():
            # Serialize taskers with their addresses
            serializer = TaskerSerializer(taskers, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({"error": "No taskers found for this service."}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def taskerdata(request):
    user = request.user
    tasker_serializer = TaskerSerializer(user)
    return Response(tasker_serializer.data, status=status.HTTP_200_OK)

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