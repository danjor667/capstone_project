import uuid
from django.db import models
from django.contrib.auth.models import User
from patients.models import Patient

class Alert(models.Model):
    ALERT_TYPES = [
        ('critical', 'Critical'),
        ('warning', 'Warning'),
        ('info', 'Info'),
    ]
    
    PRIORITY_LEVELS = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    
    CATEGORIES = [
        ('lab', 'Lab Result'),
        ('vital', 'Vital Signs'),
        ('medication', 'Medication'),
        ('appointment', 'Appointment'),
        ('system', 'System'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='alerts')
    type = models.CharField(max_length=20, choices=ALERT_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_LEVELS, default='medium')
    category = models.CharField(max_length=20, choices=CATEGORIES, default='system')
    acknowledged = models.BooleanField(default=False)
    acknowledged_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'alerts'
        indexes = [
            models.Index(fields=['patient', '-created_at']),
            models.Index(fields=['acknowledged']),
            models.Index(fields=['priority']),
        ]
        ordering = ['-created_at']

class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('system', 'System'),
        ('patient_update', 'Patient Update'),
        ('alert', 'Alert'),
        ('reminder', 'Reminder'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES)
    title = models.CharField(max_length=200)
    message = models.TextField()
    read = models.BooleanField(default=False)
    data = models.JSONField(default=dict)  # Additional notification data
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'notifications'
        indexes = [
            models.Index(fields=['user', '-created_at']),
            models.Index(fields=['read']),
        ]
        ordering = ['-created_at']