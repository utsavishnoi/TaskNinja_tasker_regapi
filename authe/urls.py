from django.urls import path, include
from . import views
from .views import UserDataView

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('register/', views.CreateUserView.as_view(), name='register'),
    path('api/userdata/', UserDataView.as_view(), name='userdata')
]
