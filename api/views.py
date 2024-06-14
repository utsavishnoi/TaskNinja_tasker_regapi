from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Tasker
from .serializers import TaskerSerializer
from django.contrib.auth.hashers import make_password

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from django.db import connection

@api_view(['POST'])
@permission_classes([AllowAny])
def register_tasker(request):
    if request.method == 'POST':
        data = request.data.copy()
        data['password'] = make_password(data['password'])
        serializer = TaskerSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            print(connection.queries)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
