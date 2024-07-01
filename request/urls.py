from django.urls import path,include
from  . import views

urlpatterns = [
    path('user/request/',views.send_req,name = 'send_request'),
    path('user/requests/',views.request_list,name = 'requestlist'),
    path('cancel/<int:req_id>',views.cancellation,name='cancellation')
]