from django.shortcuts import render
from .serializers import RequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from authe.models import CustomUser
from .models import Request

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_req(request):
    data = request.data
    request_serializer = RequestSerializer(data=data)
    
    if request_serializer.is_valid():
        user = request_serializer.validated_data.get('user')
        tasker = request_serializer.validated_data.get('tasker')
        
        try:
            requester_type = user.user_type
        except AttributeError:
            return Response({'error': f'User with id {user.id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_request_type = tasker.user_type
        except AttributeError:
            return Response({'error': f'Tasker with id {tasker.id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if requester_type == 'user' and to_request_type == 'tasker': 
            request_serializer.save()
            return Response(request_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Unauthorized request type'}, status=status.HTTP_403_FORBIDDEN)
    else:
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

from django.shortcuts import get_object_or_404

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_list_user(request, user_id):
    req_list = Request.objects.filter(user=user_id)
    user = get_object_or_404(CustomUser, id=user_id)
    if user.user_type == 'user':
        # Assuming req_list is a queryset, you might want to serialize it or process it further
        # For example, if using Django REST Framework, you might serialize req_list
        # serializer = RequestSerializer(req_list, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = RequestSerializer(req_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        # Handle case where user_type is not 'user'
        return Response(status=status.HTTP_400_BAD_REQUEST)

