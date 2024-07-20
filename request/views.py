from .serializers import RequestSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import Request
from django.utils.timezone import make_aware
from django.utils import timezone
from datetime import timedelta,datetime
from django.utils.timezone import now
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from authe.models import CustomUser
from django.utils.timezone import now

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def send_req(request):
    data = request.data
    request_serializer = RequestSerializer(data=data)
    if request_serializer.is_valid():
        user = request.user
        tasker = request_serializer.validated_data.get('tasker')
        request_date = request_serializer.validated_data.get('service_date')

        if request_date is None:
            return Response({'error': 'Service date is required'}, status=status.HTTP_400_BAD_REQUEST)

        booking_date = now()
        three_hours_after_now = booking_date + timedelta(hours=3)

        if request_date.date() < booking_date.date():
            return Response({'error': 'Cannot request with a date in the past'}, status=status.HTTP_400_BAD_REQUEST)

        if request_date > three_hours_after_now:
            return Response({'error': 'Booking must be at least 3 hours in advance'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            requester_type = user.user_type
        except AttributeError:
            return Response({'error': f'User with id {user.id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            to_request_type = tasker.user_type
        except AttributeError:
            return Response({'error': f'Tasker with id {tasker.id} does not exist'}, status=status.HTTP_400_BAD_REQUEST)

        if requester_type == 'user' and to_request_type == 'tasker':
            request_serializer.save(booking_date=booking_date)
            return Response(request_serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'Unauthorized request type'}, status=status.HTTP_403_FORBIDDEN)
    else:
        # Return detailed validation errors to frontend
        return Response(request_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def request_list(request):
    current_user_id = request.user.id
    user = request.user

    if user.user_type == 'user':
        req_list = Request.objects.filter(user=current_user_id).exclude(status__in=[3, 4, 5])
    elif user.user_type == 'tasker':
        req_list = Request.objects.filter(tasker=current_user_id).exclude(status__in=[3, 4, 5])
    else:
        return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RequestSerializer(req_list, many=True)
    response_data = serializer.data

    for item in response_data:
        user_details = CustomUser.objects.get(id=item['tasker'])
        item['tasker_name'] = user_details.first_name
        item['user_contact_number'] = user_details.contact_number

    return Response(response_data, status=status.HTTP_200_OK)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def requests_history(request):
    current_user_id = request.user.id
    user = request.user

    if user.user_type == 'user':
        req_list = Request.objects.filter(user=current_user_id).exclude(status__in=[1,2])
    elif user.user_type == 'tasker':
        req_list = Request.objects.filter(tasker=current_user_id).exclude(status__in=[1,2])
    else:
        return Response({"error": "Invalid user type."}, status=status.HTTP_400_BAD_REQUEST)

    serializer = RequestSerializer(req_list, many=True)
    response_data = serializer.data

    for item in response_data:
        user_details = CustomUser.objects.get(id=item['tasker'])
        item['user_name'] = user_details.first_name
        item['user_contact_number'] = user_details.contact_number

    return Response(response_data, status=status.HTTP_200_OK)


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def cancellation(request, req_id):
    req_instance = get_object_or_404(Request, req_id=req_id)
    current_user_id = request.user.id
    user = request.user

    if req_instance.status == 2 or user.user_type == 'user':
        if req_instance.user.id == current_user_id or req_instance.tasker.id == current_user_id:
            current_time = make_aware(datetime.now())

            # print("current--->", current_time, "type-->", type(current_time))
            
            service_date = req_instance.service_date
            cancellation_window = service_date - timedelta(hours=6)
            
            print("cancellation_window--->", cancellation_window)
            
            # Allow cancellation if the service date has passed
            if current_time > service_date:
                req_instance.status = 3
                req_instance.save()
                return Response({"message": "Request successfully cancelled."}, status=status.HTTP_200_OK)
            
            # Check if the cancellation is on the same day as the service date
            if current_time.date() == service_date.date():
                return Response({"error": "Cancellation not allowed on the same day as the service date."}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if the cancellation is within 6 hours of the service date
            if current_time >= cancellation_window:
                return Response({"error": "Cancellation not allowed within 6 hours of service date."}, status=status.HTTP_400_BAD_REQUEST)
            
            req_instance.status = 3
            req_instance.save()
            return Response({"message": "Request successfully cancelled."}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "You can't cancel this request."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({"error": "Can't cancel a request which is not booked."}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def reject_request(request, req_id):
    req_instance = get_object_or_404(Request, req_id=req_id)
    current_user = request.user

    if current_user.user_type == 'tasker' and req_instance.tasker == current_user:
        req_instance.status = 4
        req_instance.save()
        return Response({"Request Rejected !"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "You can't reject this request."},
                        status=status.HTTP_400_BAD_REQUEST)

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def accept_request(request, req_id):
    req_instance = get_object_or_404(Request, req_id=req_id)
    current_user = request.user

    if current_user.user_type == 'tasker' and req_instance.tasker == current_user:
        req_instance.status = 2
        req_instance.save()
        return Response({"Request Accepted !"}, status=status.HTTP_200_OK)
    else:
        return Response({"error": "You can't accept this request."},
                        status=status.HTTP_400_BAD_REQUEST)