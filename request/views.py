from django.shortcuts import render
from .serializers import RequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from authe.models import CustomUser
from .models import Request
from django.utils import timezone
from datetime import timedelta, datetime

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_req(request):
    data = request.data
    request_serializer = RequestSerializer(data=data)
    
    if request_serializer.is_valid():
        user = request.user
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
def request_list(request):
    current_user_id = request.user.id
    
    # Determine if the current user is a 'user' or 'tasker' based on user_type
    try:
        user = CustomUser.objects.get(id=current_user_id)
        if user.user_type == 'user':
            req_list = Request.objects.filter(user=current_user_id)
        elif user.user_type == 'tasker':
            req_list = Request.objects.filter(tasker=current_user_id)
        else:
            return Response({"error": "Invalid user type."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        serializer = RequestSerializer(req_list, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."},
                        status=status.HTTP_404_NOT_FOUND)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancellation(request, req_id):
    req_instance = get_object_or_404(Request, req_id=req_id)
    current_user_id = request.user.id  # Get ID of the currently authenticated user
    if req_instance.status == 2 or request.user.type == 'user':
        # Check if the requester is the user or tasker associated with the request
        if req_instance.user.id == current_user_id or req_instance.tasker.id == current_user_id:
            # Calculate the cancellation window (6 hours before service_date)
            cancellation_window = req_instance.service_date - timedelta(hours=6)
            
            # Check if current time is within the cancellation window
            current_time = timezone.now()
            if current_time >= cancellation_window:
                return Response({"error": "Cancellation not allowed within 6 hours of service_date."},
                                status=status.HTTP_400_BAD_REQUEST)
            
            # Update request status to indicate cancellation
            req_instance.status = 3 
            req_instance.save()
            
            return Response({"message": "Request successfully cancelled."},
                            status=status.HTTP_200_OK)
        else:
            return Response({"error": "You can't cancel this request."},
                            status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error: Can't cancel a request which is not booked"})

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reject_request(request,req_id):
      req_instance = get_object_or_404(Request,req_id=req_id)
      current_user = request.user
      if current_user.user_type == 'tasker':
          req_instance.status = 4
          req_instance.save()

          return Response({"Request Rejected !"},status=status.HTTP_200_OK)
      else:
          return Response({"error": "You can't reject this request."},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_request(request,req_id):
    req_instance = get_object_or_404(Request,req_id=req_id)
    current_user = request.user
    if current_user.user_type == 'tasker':
        req_instance.status = 2
        req_instance.save()

        return Response({"Request Accepted !"},status=status.HTTP_200_OK)
    else:
          return Response({"error": "You can't accept this request."},
                        status=status.HTTP_400_BAD_REQUEST)       