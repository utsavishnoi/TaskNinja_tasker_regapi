from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from .serializers import CustomUserSerializer,TaskerSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import CustomUser

# class CreateUserView(generics.CreateAPIView):
#     queryset = CustomUser.objects.all()
#     serializer_class = CustomUserSerializer
#     permission_classes = [AllowAny]

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    if request.method == 'POST':
        data = request.data.copy()


        # Serialize the Tasker data
        user_serializer = CustomUserSerializer(data=data)

        # Validate and save Tasker data
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

@api_view(['POST'])
@permission_classes([AllowAny])        
def register_tasker(request):
    if request.method == 'POST':
        data = request.data.copy()

        tasker_serializer = TaskerSerializer(data=data)

        if tasker_serializer.is_valid():
            tasker_serializer.save()
            return Response(tasker_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(tasker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomeView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)

@api_view(['GET'])
@permission_classes([AllowAny])
def list_taskers_by_service(request, service_name):
    try:
        taskers = CustomUser.objects.filter(user_type='tasker', service=service_name).values('first_name', 'last_name', 'service', 'contact_number', 'about','price')
        if taskers.exists():
            return Response(taskers, status=status.HTTP_200_OK)
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