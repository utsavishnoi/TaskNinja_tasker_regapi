from django.urls import path, include
from . import views
from .views import UserDataView,AddressUpdateView,AddressCreateView,delete_user

urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('user/register/',views.register_user,name = 'register user'),
    path('tasker/register/',views.register_tasker,name ='register tasker'),
    path('taskers/<str:service_name>/',views.list_taskers_by_service,name='list taskers'),
    path('tasker/data/',views.taskerdata,name="tasker data"),
    path('user/data/', UserDataView.as_view(), name='userdata'),
    path('tasker/data/delete/<int:user_id>',views.delete_tasker,name="delete tasker"),
    path('tasker/update/<int:user_id>', views.update_tasker,name='update_tasker_data'),
    path('api/addresses/update/<str:id>/', AddressUpdateView.as_view(), name='address-update'),
    path('api/addresses/delete/<int:id>/',delete_user , name='address-delete'),
    path('users/<str:username>/addresses/', AddressCreateView.as_view(), name='address-create'),
    ]