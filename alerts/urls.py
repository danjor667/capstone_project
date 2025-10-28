from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import AlertViewSet, NotificationViewSet

router = DefaultRouter()
router.register(r'notifications', NotificationViewSet, basename='notification')

urlpatterns = [
    path('patients/<uuid:pk>/alerts/', AlertViewSet.as_view({
        'get': 'patient_alerts'
    }), name='patient-alerts'),
    path('alerts/', AlertViewSet.as_view({
        'post': 'create'
    }), name='create-alert'),
    path('alerts/<uuid:pk>/acknowledge/', AlertViewSet.as_view({
        'put': 'acknowledge_alert'
    }), name='acknowledge-alert'),
    path('alerts/<uuid:pk>/', AlertViewSet.as_view({
        'delete': 'destroy'
    }), name='dismiss-alert'),
    path('', include(router.urls)),
]