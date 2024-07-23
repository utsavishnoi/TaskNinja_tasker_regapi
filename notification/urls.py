from django.urls import path
from .views import get_notification

urlpatterns = [
    path('user/notifications',get_notification,name="get_notifications")
]