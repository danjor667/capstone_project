from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import MedicalDataViewSet, MedicationViewSet

router = DefaultRouter()
router.register(r'medications', MedicationViewSet)

urlpatterns = [
    path('patients/<uuid:pk>/metrics/', MedicalDataViewSet.as_view({
        'get': 'kidney_metrics',
        'post': 'kidney_metrics'
    }), name='patient-metrics'),
    path('patients/<uuid:pk>/metrics/history/', MedicalDataViewSet.as_view({
        'get': 'metrics_history'
    }), name='patient-metrics-history'),
    path('patients/<uuid:pk>/lab-results/', MedicalDataViewSet.as_view({
        'get': 'lab_results',
        'post': 'lab_results'
    }), name='patient-lab-results'),
    path('patients/<uuid:pk>/medications/', MedicalDataViewSet.as_view({
        'get': 'medications',
        'post': 'medications'
    }), name='patient-medications'),
    path('patients/<uuid:pk>/vitals/', MedicalDataViewSet.as_view({
        'get': 'vital_signs',
        'post': 'vital_signs'
    }), name='patient-vitals'),
    path('', include(router.urls)),
]