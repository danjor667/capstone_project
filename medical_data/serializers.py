from rest_framework import serializers
from .models import KidneyMetrics, LabResult, Medication, VitalSigns
from django.utils import timezone

class KidneyMetricsSerializer(serializers.ModelSerializer):
    blood_pressure = serializers.SerializerMethodField()
    progression = serializers.SerializerMethodField()
    timestamp = serializers.DateTimeField(required=False)
    
    class Meta:
        model = KidneyMetrics
        fields = [
            'id', 'timestamp', 'egfr', 'creatinine', 'proteinuria',
            'blood_pressure', 'stage', 'progression', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']
    
    def create(self, validated_data):
        if 'timestamp' not in validated_data:
            validated_data['timestamp'] = timezone.now()
        return super().create(validated_data)
    
    def get_blood_pressure(self, obj):
        return {
            'systolic': obj.systolic_bp,
            'diastolic': obj.diastolic_bp
        }
    
    def get_progression(self, obj):
        return {
            'trend': obj.trend,
            'rateOfChange': float(obj.rate_of_change),
            'predictedStage': obj.predicted_stage,
            'timeToNextStage': obj.time_to_next_stage
        }

class LabResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = LabResult
        fields = [
            'id', 'test_name', 'value', 'unit', 'reference_range',
            'test_date', 'is_abnormal', 'category', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = [
            'id', 'name', 'dosage', 'frequency', 'start_date',
            'end_date', 'is_active', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

class VitalSignsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VitalSigns
        fields = [
            'id', 'timestamp', 'systolic_bp', 'diastolic_bp',
            'heart_rate', 'temperature', 'weight', 'height', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']