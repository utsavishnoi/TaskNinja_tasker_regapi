from django.urls import path,include
from  . import views

urlpatterns = [
    path('user/request/',views.send_req,name = 'send_request'),
    path('user/requests/<int:user_id>',views.request_list_user,name = 'requestlist_user')
]