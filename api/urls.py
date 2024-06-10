from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import CompanyViewSet, UserViewSet

router = DefaultRouter()
router.register(r'companies', CompanyViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    
]
