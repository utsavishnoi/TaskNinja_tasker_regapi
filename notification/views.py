from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from request.models import Request
from .models import Notification
from django.shortcuts import get_object_or_404





@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification(request):
    current_user = request.user
    if current_user.user_type == "user":
        req_list = Request.objects.filter(user=current_user.id)
    else:
        req_list = Request.objects.filter(tasker=current_user.id)
    
    # Order notifications by creation date (newest first)
    notifications = Notification.objects.filter(request__in=req_list, user=current_user).order_by('-created_at')
    serializer = NotificationSerializer(notifications, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)



def create_notification(user, req_instance, message):
    Notification.objects.create(
        user=user,
        request=req_instance,
        message=message,
    )


@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def read_notification(request,notification_id):
    user = request.user
    notification = get_object_or_404(Notification, notification_id=notification_id, user = user )
    notification.status = 1
    notification.save()
    return Response({"message": "Notification marked as read"}, status=status.HTTP_200_OK)
