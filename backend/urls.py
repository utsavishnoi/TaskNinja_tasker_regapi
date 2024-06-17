from django.contrib import admin
from django.urls import path,include
from authe.views import UserDataView
from rest_framework_simplejwt.views import TokenRefreshView,TokenObtainPairView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/',TokenObtainPairView.as_view(),name="get_token"),
    path('api/token/refresh/',TokenRefreshView.as_view(),name="refresh"),
    path('api-auth/',include("rest_framework.urls")),
    path('',include('authe.urls')),
    path('',include('api.urls')),
    path('api/userdata/', UserDataView.as_view(), name='user-data'),
    
]
