from django.urls import path
from .views import register_tasker

urlpatterns = [
    path('api/v1/taskers/', register_tasker, name='register_tasker'),
]
