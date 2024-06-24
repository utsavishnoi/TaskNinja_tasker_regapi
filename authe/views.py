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
@permission_classes([IsAuthenticated])
def list_taskers_by_service(request, service_name):
    try:
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

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def userdata(request):
    user = request.user
    user_serializer = CustomUserSerializer(user)
    return Response(user_serializer.data, status=status.HTTP_200_OK)

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


