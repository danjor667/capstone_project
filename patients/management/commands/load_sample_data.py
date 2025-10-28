from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from patients.models import Patient, MedicalHistory
from medical_data.models import KidneyMetrics, LabResult, VitalSigns
from alerts.models import Alert
import pandas as pd
from datetime import datetime, timedelta
import random

class Command(BaseCommand):
    help = 'Load sample data from CKD dataset'
    
    def handle(self, *args, **options):
        self.stdout.write('Loading sample data...')
        
        # Create superuser if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user')
        
        # Load CKD dataset
        try:
            df = pd.read_csv('ML/Chronic_Kidney_Dsease_data.csv')
            self.stdout.write(f'Loaded {len(df)} records from dataset')
            
            # Create sample patients from first 10 records
            for i, row in df.head(10).iterrows():
                # Create patient
                patient = Patient.objects.create(
                    first_name=f'Patient{i+1}',
                    last_name='Sample',
                    date_of_birth=datetime.now().date() - timedelta(days=int(row['Age'])*365),
                    gender='male' if row['Gender'] == 1 else 'female',
                    email=f'patient{i+1}@example.com'
                )
                
                # Create medical history
                MedicalHistory.objects.create(
                    patient=patient,
                    conditions=['Chronic Kidney Disease'] if row['Diagnosis'] == 1 else [],
                    family_history=['Hypertension'] if row.get('FamilyHistoryHypertension', 0) == 1 else []
                )
                
                # Create kidney metrics
                KidneyMetrics.objects.create(
                    patient=patient,
                    timestamp=datetime.now(),
                    egfr=row['GFR'],
                    creatinine=row['SerumCreatinine'],
                    proteinuria=row.get('ProteinInUrine', 0),
                    systolic_bp=int(row['SystolicBP']),
                    diastolic_bp=int(row['DiastolicBP']),
                    stage=min(5, max(1, int(row['GFR'] / 20))),  # Simple stage calculation
                    trend='declining' if row['GFR'] < 60 else 'stable'
                )
                
                # Create lab results
                lab_tests = [
                    ('Serum Creatinine', row['SerumCreatinine'], 'mg/dL'),
                    ('BUN', row['BUNLevels'], 'mg/dL'),
                    ('Hemoglobin', row['HemoglobinLevels'], 'g/dL'),
                    ('Total Cholesterol', row['CholesterolTotal'], 'mg/dL')
                ]
                
                for test_name, value, unit in lab_tests:
                    LabResult.objects.create(
                        patient=patient,
                        test_name=test_name,
                        value=value,
                        unit=unit,
                        test_date=datetime.now(),
                        category='kidney' if 'Creatinine' in test_name or 'BUN' in test_name else 'blood'
                    )
                
                # Create vital signs
                VitalSigns.objects.create(
                    patient=patient,
                    timestamp=datetime.now(),
                    systolic_bp=int(row['SystolicBP']),
                    diastolic_bp=int(row['DiastolicBP']),
                    heart_rate=random.randint(60, 100),
                    weight=random.uniform(50, 100)
                )
                
                # Create alerts for high-risk patients
                if row['GFR'] < 30:
                    Alert.objects.create(
                        patient=patient,
                        type='critical',
                        title='Critical eGFR Level',
                        message=f'Patient eGFR is {row["GFR"]:.1f}, indicating severe kidney dysfunction',
                        priority='critical',
                        category='lab'
                    )
                
                self.stdout.write(f'Created patient {patient.first_name} {patient.last_name}')
            
            self.stdout.write(self.style.SUCCESS('Successfully loaded sample data'))
            
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR('CKD dataset file not found. Please ensure ML/Chronic_Kidney_Dsease_data.csv exists'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading data: {str(e)}'))