from rest_framework import serializers
from .models import Patient, MedicalHistory

class MedicalHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = MedicalHistory
        fields = ['conditions', 'allergies', 'family_history']

class PatientSerializer(serializers.ModelSerializer):
    medical_history = MedicalHistorySerializer(read_only=True)
    age = serializers.SerializerMethodField()
    
    class Meta:
        model = Patient
        fields = [
            'id', 'first_name', 'last_name', 'date_of_birth', 'gender',
            'ethnicity', 'email', 'phone', 'street', 'city', 'state',
            'zip_code', 'country', 'medical_history', 'age', 'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def get_age(self, obj):
        from datetime import date
        today = date.today()
        return today.year - obj.date_of_birth.year - ((today.month, today.day) < (obj.date_of_birth.month, obj.date_of_birth.day))

class PatientCreateSerializer(serializers.ModelSerializer):
    medical_history = MedicalHistorySerializer(required=False)
    
    class Meta:
        model = Patient
        fields = [
            'first_name', 'last_name', 'date_of_birth', 'gender',
            'ethnicity', 'email', 'phone', 'street', 'city', 'state',
            'zip_code', 'country', 'medical_history'
        ]
    
    def create(self, validated_data):
        medical_history_data = validated_data.pop('medical_history', {})
        patient = Patient.objects.create(**validated_data)
        MedicalHistory.objects.create(patient=patient, **medical_history_data)
        return patient