from django.urls import path,include
from  . import views
urlpatterns = [
    path('home/', views.HomeView.as_view(), name ='home'),
    path('user/register/',views.register_user,name = 'register user'),
    path('user/data/',views.userdata,name = 'user_data'),
    path('tasker/register/',views.register_tasker,name ='register tasker'),
    path('taskers/<str:service_name>/',views.list_taskers_by_service,name='list taskers'),
    path('tasker/data/',views.taskerdata,name="tasker data"),
    path('tasker/data/delete/<int:user_id>',views.delete_tasker,name="delete tasker"),
    path('tasker/update/<int:user_id>', views.update_tasker,name='update_tasker_data')
]