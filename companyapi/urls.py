from django.contrib import admin
from django.urls import path, include
from .views import home_page
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", home_page),
    path("api/v1/", include('api.urls')),
]


