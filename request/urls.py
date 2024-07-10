from django.urls import path,include
from  . import views

urlpatterns = [
    path('user/request/',views.send_req,name = 'send_request'),
    path('requests/',views.request_list,name = 'requestlist'),
    path('cancel/<int:req_id>',views.cancellation,name='cancellation'),
    path('tasker/reject/<int:req_id>',views.reject_request,name='reject_request'),
    path('tasker/accept/<int:req_id>',views.accept_request,name='accept request'),
    path('requests/history/',views.requests_history,name='cancelled_requests'),

]