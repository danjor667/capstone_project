import uuid
from django.db import models
from patients.models import Patient

class KidneyMetrics(models.Model):
    STAGE_CHOICES = [
        (1, 'Stage 1'),
        (2, 'Stage 2'),
        (3, 'Stage 3'),
        (4, 'Stage 4'),
        (5, 'Stage 5'),
    ]
    
    TREND_CHOICES = [
        ('improving', 'Improving'),
        ('stable', 'Stable'),
        ('declining', 'Declining'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='kidney_metrics')
    timestamp = models.DateTimeField()
    egfr = models.DecimalField(max_digits=5, decimal_places=2)
    creatinine = models.DecimalField(max_digits=4, decimal_places=2)
    proteinuria = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    systolic_bp = models.IntegerField(null=True, blank=True)
    diastolic_bp = models.IntegerField(null=True, blank=True)
    stage = models.IntegerField(choices=STAGE_CHOICES)
    
    # Progression data
    trend = models.CharField(max_length=20, choices=TREND_CHOICES, default='stable')
    rate_of_change = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    predicted_stage = models.IntegerField(choices=STAGE_CHOICES, null=True, blank=True)
    time_to_next_stage = models.IntegerField(null=True, blank=True)  # days
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'kidney_metrics'
        indexes = [
            models.Index(fields=['patient', '-timestamp']),
        ]
        ordering = ['-timestamp']

class LabResult(models.Model):
    CATEGORY_CHOICES = [
        ('kidney', 'Kidney'),
        ('blood', 'Blood'),
        ('urine', 'Urine'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='lab_results')
    test_name = models.CharField(max_length=100)
    value = models.DecimalField(max_digits=10, decimal_places=4)
    unit = models.CharField(max_length=20)
    reference_range = models.CharField(max_length=50, blank=True, null=True)
    test_date = models.DateTimeField()
    is_abnormal = models.BooleanField(default=False)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='other')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'lab_results'
        indexes = [
            models.Index(fields=['patient', '-test_date']),
            models.Index(fields=['test_name']),
        ]

class Medication(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='medications')
    name = models.CharField(max_length=200)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'medications'

class VitalSigns(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='vital_signs')
    timestamp = models.DateTimeField()
    systolic_bp = models.IntegerField()
    diastolic_bp = models.IntegerField()
    heart_rate = models.IntegerField(null=True, blank=True)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    weight = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    height = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'vital_signs'
        indexes = [
            models.Index(fields=['patient', '-timestamp']),
        ]