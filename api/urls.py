from django.urls import path
from .views import register_tasker,list_taskers_by_service

urlpatterns = [
    path('taskers/register/', register_tasker, name='register_tasker'),
    path('api/taskers/<str:service_name>/', list_taskers_by_service, name='list_taskers_by_service'),
]
