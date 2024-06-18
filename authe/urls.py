from django.urls import path, include
from . import views
from .views import UserDataView,AddressUpdateView

urlpatterns = [
    path('home/', views.HomeView.as_view(), name='home'),
    path('register/',views.register_user,name = 'register'),
    path('api/userdata/', UserDataView.as_view(), name='userdata'),
    path('api/addresses/<int:id>/', AddressUpdateView.as_view(), name='address-update')
    
    ]
