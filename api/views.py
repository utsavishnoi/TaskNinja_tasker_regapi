from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import make_password
from .serializers import TaskerSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_tasker(request):
    if request.method == 'POST':
        data = request.data.copy()
        
        # Hash the password before saving
        data['password'] = make_password(data['password'])
        
        # Serialize the Tasker data
        tasker_serializer = TaskerSerializer(data=data)
        
        # Validate and save Tasker data
        if tasker_serializer.is_valid():
            tasker_serializer.save()
            return Response(tasker_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(tasker_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
