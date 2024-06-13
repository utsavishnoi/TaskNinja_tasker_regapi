from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import TaskerViewSet, UserViewSet, TaskerLoginView

router = DefaultRouter()
router.register(r'taskers', TaskerViewSet)
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('login/tasker/', TaskerLoginView.as_view(), name='tasker-login'),
]
