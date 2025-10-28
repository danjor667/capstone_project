import uuid
from django.db import models
from patients.models import Patient

class MLPrediction(models.Model):
    RISK_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='ml_predictions')
    prediction_result = models.CharField(max_length=100)
    confidence = models.DecimalField(max_digits=5, decimal_places=2)
    predicted_stage = models.IntegerField(null=True, blank=True)
    risk_level = models.CharField(max_length=20, choices=RISK_LEVELS)
    input_data = models.JSONField()
    recommendations = models.JSONField(default=list)
    model_version = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ml_predictions'
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['risk_level']),
        ]
        ordering = ['-created_at']

class RiskFactor(models.Model):
    FACTOR_TYPES = [
        ('lifestyle', 'Lifestyle'),
        ('medical', 'Medical'),
        ('genetic', 'Genetic'),
        ('environmental', 'Environmental'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='risk_factors')
    factor_name = models.CharField(max_length=100)
    factor_type = models.CharField(max_length=20, choices=FACTOR_TYPES)
    impact_score = models.DecimalField(max_digits=4, decimal_places=2)  # 0-100
    description = models.TextField()
    is_modifiable = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'risk_factors'

class TrendAnalysis(models.Model):
    TREND_TYPES = [
        ('egfr', 'eGFR Trend'),
        ('creatinine', 'Creatinine Trend'),
        ('blood_pressure', 'Blood Pressure Trend'),
        ('overall', 'Overall Health Trend'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='trend_analyses')
    trend_type = models.CharField(max_length=20, choices=TREND_TYPES)
    trend_data = models.JSONField()  # Time series data
    slope = models.DecimalField(max_digits=8, decimal_places=4)
    r_squared = models.DecimalField(max_digits=4, decimal_places=3)
    prediction_horizon_days = models.IntegerField(default=90)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'trend_analyses'