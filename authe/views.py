from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import CustomUser
from .serializers import CustomUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db import connection
from rest_framework import status





class CreateUserView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny]

class HomeView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': 'Welcome to the JWT Authentication page using React Js and Django!'}
        return Response(content)
    
class UserDataView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user #
        serializer = CustomUserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


