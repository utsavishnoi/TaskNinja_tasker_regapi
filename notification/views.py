from .serializers import NotificationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from request.models import Request
from .models import Notification
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notification(request):
    current_user = request.user
    if current_user.user_type == "user":
        req_list = Request.objects.filter(user=current_user.id)
    else:
        req_list = Request.objects.filter(tasker=current_user.id)
    
    notifications = Notification.objects.filter(request__in=req_list, user=current_user)
    serializer = NotificationSerializer(notifications, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)



def create_notification(user, req_instance, message):
    Notification.objects.create(
        user=user,
        request=req_instance,
        message=message,
    )