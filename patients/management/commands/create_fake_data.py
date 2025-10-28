from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from patients.models import Patient, MedicalHistory
from medical_data.models import KidneyMetrics, LabResult, Medication, VitalSigns
from ml_predictions.models import MLPrediction, RiskFactor, TrendAnalysis
from alerts.models import Alert, Notification
from datetime import datetime, timedelta, date
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Create comprehensive fake data for CKD Digital Twin Dashboard'
    
    def add_arguments(self, parser):
        parser.add_argument('--patients', type=int, default=20, help='Number of patients to create')
        parser.add_argument('--clear', action='store_true', help='Clear existing data first')
    
    def handle(self, *args, **options):
        if options['clear']:
            self.stdout.write('Clearing existing data...')
            Patient.objects.all().delete()
            
        num_patients = options['patients']
        self.stdout.write(f'Creating {num_patients} fake patients with complete data...')
        
        # Create admin user if not exists
        if not User.objects.filter(username='admin').exists():
            User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
            self.stdout.write('Created admin user')
        
        for i in range(num_patients):
            patient = self.create_patient()
            self.create_medical_history(patient)
            self.create_kidney_metrics(patient)
            self.create_lab_results(patient)
            self.create_medications(patient)
            self.create_vital_signs(patient)
            self.create_ml_predictions(patient)
            self.create_risk_factors(patient)
            self.create_alerts(patient)
            
            self.stdout.write(f'Created patient {i+1}: {patient.first_name} {patient.last_name}')
        
        self.stdout.write(self.style.SUCCESS(f'Successfully created {num_patients} patients with complete data'))
    
    def create_patient(self):
        gender = random.choice(['male', 'female'])
        first_name = fake.first_name_male() if gender == 'male' else fake.first_name_female()
        
        return Patient.objects.create(
            first_name=first_name,
            last_name=fake.last_name(),
            date_of_birth=fake.date_of_birth(minimum_age=25, maximum_age=85),
            gender=gender,
            ethnicity=random.choice(['Caucasian', 'African American', 'Hispanic', 'Asian', 'Other']),
            email=fake.email(),
            phone=fake.phone_number()[:20],
            street=fake.street_address(),
            city=fake.city(),
            state=fake.state_abbr(),
            zip_code=fake.zipcode(),
            country='USA'
        )
    
    def create_medical_history(self, patient):
        conditions = random.sample([
            'Hypertension', 'Diabetes Type 2', 'Heart Disease', 
            'Chronic Kidney Disease', 'Obesity', 'High Cholesterol'
        ], k=random.randint(1, 3))
        
        allergies = random.sample([
            'Penicillin', 'Shellfish', 'Nuts', 'Latex', 'Aspirin'
        ], k=random.randint(0, 2))
        
        family_history = random.sample([
            'Kidney Disease', 'Diabetes', 'Hypertension', 'Heart Disease'
        ], k=random.randint(0, 2))
        
        return MedicalHistory.objects.create(
            patient=patient,
            conditions=conditions,
            allergies=allergies,
            family_history=family_history
        )
    
    def create_kidney_metrics(self, patient):
        # Create historical data (last 12 months)
        for i in range(12):
            timestamp = datetime.now() - timedelta(days=30*i)
            
            # Simulate disease progression
            base_egfr = random.uniform(15, 120)
            egfr = max(15, base_egfr - (i * random.uniform(0, 2)))
            
            # Calculate stage based on eGFR
            if egfr >= 90:
                stage = 1
            elif egfr >= 60:
                stage = 2
            elif egfr >= 30:
                stage = 3
            elif egfr >= 15:
                stage = 4
            else:
                stage = 5
            
            creatinine = random.uniform(0.8, 5.0)
            if stage >= 3:
                creatinine = random.uniform(1.5, 5.0)
            
            KidneyMetrics.objects.create(
                patient=patient,
                timestamp=timestamp,
                egfr=round(egfr, 2),
                creatinine=round(creatinine, 2),
                proteinuria=round(random.uniform(0, 3.0), 2),
                systolic_bp=random.randint(110, 180),
                diastolic_bp=random.randint(70, 110),
                stage=stage,
                trend=random.choice(['improving', 'stable', 'declining']),
                rate_of_change=round(random.uniform(-5, 5), 2),
                predicted_stage=min(5, stage + random.randint(0, 1)),
                time_to_next_stage=random.randint(30, 365) if stage < 5 else None
            )
    
    def create_lab_results(self, patient):
        tests = [
            ('Serum Creatinine', 'mg/dL', (0.8, 5.0), 'kidney'),
            ('BUN', 'mg/dL', (10, 80), 'kidney'),
            ('Hemoglobin', 'g/dL', (10, 16), 'blood'),
            ('Total Cholesterol', 'mg/dL', (150, 300), 'blood'),
            ('LDL Cholesterol', 'mg/dL', (70, 200), 'blood'),
            ('HDL Cholesterol', 'mg/dL', (30, 80), 'blood'),
            ('Triglycerides', 'mg/dL', (50, 400), 'blood'),
            ('Glucose', 'mg/dL', (70, 200), 'blood'),
            ('Protein in Urine', 'mg/dL', (0, 300), 'urine'),
        ]
        
        for i in range(random.randint(5, 15)):
            test_name, unit, (min_val, max_val), category = random.choice(tests)
            value = round(random.uniform(min_val, max_val), 2)
            
            # Determine if abnormal based on rough normal ranges
            is_abnormal = False
            if test_name == 'Serum Creatinine' and value > 1.3:
                is_abnormal = True
            elif test_name == 'BUN' and value > 20:
                is_abnormal = True
            elif test_name == 'Hemoglobin' and value < 12:
                is_abnormal = True
            
            LabResult.objects.create(
                patient=patient,
                test_name=test_name,
                value=value,
                unit=unit,
                reference_range=f'{min_val}-{max_val}',
                test_date=fake.date_time_between(start_date='-6M', end_date='now'),
                is_abnormal=is_abnormal,
                category=category
            )
    
    def create_medications(self, patient):
        medications = [
            ('Lisinopril', '10mg', 'Once daily'),
            ('Metformin', '500mg', 'Twice daily'),
            ('Amlodipine', '5mg', 'Once daily'),
            ('Atorvastatin', '20mg', 'Once daily'),
            ('Furosemide', '40mg', 'Once daily'),
            ('Metoprolol', '50mg', 'Twice daily'),
        ]
        
        for i in range(random.randint(2, 5)):
            name, dosage, frequency = random.choice(medications)
            
            Medication.objects.create(
                patient=patient,
                name=name,
                dosage=dosage,
                frequency=frequency,
                start_date=fake.date_between(start_date='-2y', end_date='now'),
                end_date=fake.date_between(start_date='now', end_date='+1y') if random.choice([True, False]) else None,
                is_active=random.choice([True, True, True, False]),  # 75% active
                notes=fake.sentence() if random.choice([True, False]) else ''
            )
    
    def create_vital_signs(self, patient):
        for i in range(random.randint(5, 20)):
            VitalSigns.objects.create(
                patient=patient,
                timestamp=fake.date_time_between(start_date='-3M', end_date='now'),
                systolic_bp=random.randint(110, 180),
                diastolic_bp=random.randint(70, 110),
                heart_rate=random.randint(60, 100),
                temperature=round(random.uniform(97.0, 101.0), 1),
                weight=round(random.uniform(120, 250), 2),
                height=round(random.uniform(150, 190), 2)
            )
    
    def create_ml_predictions(self, patient):
        # Get latest kidney metrics for realistic prediction
        latest_metrics = KidneyMetrics.objects.filter(patient=patient).order_by('-timestamp').first()
        
        if latest_metrics:
            stage = latest_metrics.stage
            confidence = round(random.uniform(75, 95), 2)
            
            risk_levels = ['low', 'medium', 'high', 'critical']
            risk_level = risk_levels[min(stage-1, 3)]
            
            recommendations = []
            if stage >= 3:
                recommendations.extend([
                    'Regular nephrology follow-up recommended',
                    'Monitor blood pressure closely',
                    'Consider dietary protein restriction'
                ])
            if stage >= 4:
                recommendations.extend([
                    'Prepare for renal replacement therapy',
                    'Discuss dialysis options'
                ])
            
            MLPrediction.objects.create(
                patient=patient,
                prediction_result=f'CKD Stage {stage}',
                confidence=confidence,
                predicted_stage=stage,
                risk_level=risk_level,
                input_data={
                    'age': (date.today() - patient.date_of_birth).days // 365,
                    'egfr': float(latest_metrics.egfr),
                    'creatinine': float(latest_metrics.creatinine),
                    'blood_pressure': f'{latest_metrics.systolic_bp}/{latest_metrics.diastolic_bp}'
                },
                recommendations=recommendations,
                model_version='1.0.0'
            )
    
    def create_risk_factors(self, patient):
        risk_factors = [
            ('Age', 'medical', 'Age is a significant risk factor for CKD progression'),
            ('Hypertension', 'medical', 'High blood pressure can damage kidney blood vessels'),
            ('Diabetes', 'medical', 'Diabetes is the leading cause of kidney disease'),
            ('Smoking', 'lifestyle', 'Smoking reduces blood flow to the kidneys'),
            ('Obesity', 'lifestyle', 'Excess weight increases risk of diabetes and hypertension'),
            ('Family History', 'genetic', 'Genetic predisposition to kidney disease'),
        ]
        
        for i in range(random.randint(2, 4)):
            factor_name, factor_type, description = random.choice(risk_factors)
            
            RiskFactor.objects.create(
                patient=patient,
                factor_name=factor_name,
                factor_type=factor_type,
                impact_score=round(random.uniform(20, 90), 2),
                description=description,
                is_modifiable=factor_type in ['lifestyle', 'medical']
            )
    
    def create_alerts(self, patient):
        # Create some alerts based on patient condition
        latest_metrics = KidneyMetrics.objects.filter(patient=patient).order_by('-timestamp').first()
        
        if latest_metrics and latest_metrics.egfr < 30:
            Alert.objects.create(
                patient=patient,
                type='critical',
                title='Critical eGFR Level',
                message=f'Patient eGFR is {latest_metrics.egfr}, indicating severe kidney dysfunction',
                priority='critical',
                category='lab',
                acknowledged=random.choice([True, False])
            )
        
        if latest_metrics and latest_metrics.systolic_bp > 160:
            Alert.objects.create(
                patient=patient,
                type='warning',
                title='High Blood Pressure',
                message=f'Systolic BP is {latest_metrics.systolic_bp} mmHg - requires attention',
                priority='high',
                category='vital',
                acknowledged=random.choice([True, False])
            )
        
        # Random system alerts
        if random.choice([True, False]):
            Alert.objects.create(
                patient=patient,
                type=random.choice(['info', 'warning']),
                title='Medication Reminder',
                message='Patient medication schedule needs review',
                priority=random.choice(['low', 'medium']),
                category='medication',
                acknowledged=random.choice([True, False])
            )