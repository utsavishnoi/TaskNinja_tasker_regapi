from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskerViewSet

router = DefaultRouter()
router.register(r'taskers', TaskerViewSet)


urlpatterns = [
    path('', include(router.urls)),
]
