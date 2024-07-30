from django.urls import path
from .views import get_notification,read_notification,delete_notification

urlpatterns = [
    path('user/notifications',get_notification,name="get_notifications"),
    path('notification/open/<int:notification_id>',read_notification,name="read_notification"),
    path('notification/delete/<int:notification_id>',delete_notification,name="delete_notification")
]