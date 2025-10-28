from django.urls import path
from . import views

urlpatterns = [
    path('model/metrics/', views.get_model_metrics, name='model-metrics'),
    path('patients/<uuid:patient_id>/predictions/history/', views.get_patient_prediction_history, name='patient-prediction-history'),
    path('patients/<uuid:patient_id>/analyze/', views.analyze_patient, name='analyze-patient'),
    path('patients/<uuid:patient_id>/prediction/', views.get_patient_prediction, name='patient-prediction'),
]