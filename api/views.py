from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from rest_framework.authtoken.models import Token
from .models import Tasker, User
from .serializers import TaskerSerializer, UserSerializer
from django.shortcuts import render


class TaskerLoginView(APIView):
    def get(self, request, *args, **kwargs):
        # Render the login form (assuming you have a 'login.html' template)
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'error': 'Email and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            tasker = Tasker.objects.get(email=email)
        except Tasker.DoesNotExist:
            return Response({'error': 'Tasker not found'}, status=status.HTTP_404_NOT_FOUND)

        if check_password(password, tasker.password):
            serializer = TaskerSerializer(tasker)
            return Response(serializer.data)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

    
class TaskerViewSet(viewsets.ModelViewSet):
    queryset = Tasker.objects.all()
    serializer_class = TaskerSerializer
    
    # Your additional actions can go here

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

