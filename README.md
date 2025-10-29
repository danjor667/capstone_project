# CKD Digital Twin Dashboard 🏥

> **Live Demo**: [https://capstone-web-5i4r.onrender.com/](https://capstone-web-5i4r.onrender.com/)
> 
> **Video Presentation**: [https://www.loom.com/share/afcaa53764a34c4882b647bd6feae824](https://www.loom.com/share/afcaa53764a34c4882b647bd6feae824)
> 
> **Frontend Repository**: The frontend part of this project is available at [https://github.com/danjor667/capstone_web.git](https://github.com/danjor667/capstone_web.git)

### Frontend Setup
To run the complete application with frontend:

1. **Clone the frontend repository**
```bash
git clone https://github.com/danjor667/capstone_web.git
cd capstone_web
```

2. **Update API URL**
Replace `https://capstone-project-yb98.onrender.com` with `http://localhost:8000` in the frontend API configuration.

3. **Start frontend**
```bash
npm run dev
```

A comprehensive **Chronic Kidney Disease (CKD) Digital Twin Dashboard** that combines machine learning, real-time monitoring, and 3D visualization for advanced CKD patient management and clinical decision support.

## 🎯 Overview

This capstone project delivers a complete healthcare solution that enables healthcare providers to:
- **Predict CKD risk** using AI with 92.47% accuracy
- **Monitor patient progression** in real-time
- **Visualize kidney health** through 3D models
- **Receive clinical recommendations** based on ML analysis
- **Track medical data** comprehensively

## 🏗️ Architecture

- **Backend**: Django REST API with SQLite database
- **ML Engine**: Scikit-learn with PCA-optimized Gradient Boosting (92.47% accuracy)
- **Real-time**: WebSocket support for live updates
- **3D Visualization**: Three.js integration for kidney models
- **Authentication**: JWT-based security
- **API Documentation**: Swagger/OpenAPI integration

## 🤖 Machine Learning Features

### Model Performance
- **Algorithm**: Gradient Boosting Classifier
- **Accuracy**: 92.47%
- **Precision**: 94.03%
- **Recall**: 98.03%
- **F1-Score**: 95.99%
- **AUC**: 81.81%

### Feature Engineering
- **PCA-Enhanced**: 15 optimized features from 52 original features
- **Key Features**: BMI, GFR, Serum Creatinine, HbA1c, Blood Pressure, etc.
- **Real-time Predictions**: On-demand ML analysis with confidence scores

## 📊 Key Features

### Patient Management
- Complete patient profiles with demographics
- Medical history tracking
- Search and filtering capabilities
- UUID-based secure identification

### Medical Data Tracking
- **Kidney Metrics**: eGFR, creatinine, proteinuria
- **Lab Results**: Categorized test results with abnormal value detection
- **Vital Signs**: Blood pressure, heart rate, weight monitoring
- **Medications**: Active medication tracking with dosage management

### AI-Powered Analytics
- **Risk Assessment**: 5-stage CKD classification
- **Progression Tracking**: Disease advancement monitoring
- **Personalized Recommendations**: Clinical guidelines based on patient data
- **Trend Analysis**: Historical data visualization and predictions

### Real-time Features
- **WebSocket Integration**: Live data updates
- **Alert System**: Critical value notifications
- **Notification Management**: Acknowledgment and dismissal system

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd capstone_project
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the build script**
```bash
chmod +x build.sh
./build.sh
```

4. **Start the server**
```bash
python3 manage.py runserver
```

The application will be available at `http://localhost:8000`

### Default Admin Access
- **Email**: admin@gmail.com
- **Password**: 1234



## 🏃 Running the Project Locally

### Start Development Server
```bash
# Start the Django development server
python3 manage.py runserver
```

### Access the Application
- **Application**: `http://localhost:8000`
- **API Base**: `http://localhost:8000/api/`
- **Admin Panel**: `http://localhost:8000/admin/`
- **API Documentation**: `http://localhost:8000/api/docs/`

### Test the API
```bash
# Test authentication
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@gmail.com","password":"1234"}'

# Test ML model metrics
curl -X GET http://localhost:8000/api/ml/model/metrics/ \
  -H "Authorization: Bearer <your-token>"
```

## 📡 API Endpoints

### Authentication
- `POST /api/auth/login/` - User login
- `POST /api/auth/refresh/` - Token refresh
- `GET /api/auth/me/` - Current user info

### Patient Management
- `GET /api/patients/` - List patients
- `POST /api/patients/` - Create patient
- `GET /api/patients/{id}/` - Patient details
- `PUT /api/patients/{id}/` - Update patient

### Medical Data
- `GET /api/patients/{id}/metrics/` - Latest kidney metrics
- `POST /api/patients/{id}/metrics/` - Add new metrics
- `GET /api/patients/{id}/lab-results/` - Lab results
- `GET /api/patients/{id}/medications/` - Medications

### ML Predictions
- `GET /api/ml/model/metrics/` - Model performance metrics
- `POST /api/ml/patients/{id}/analyze/` - Trigger ML analysis
- `GET /api/ml/patients/{id}/prediction/` - Latest prediction
- `GET /api/ml/patients/{id}/predictions/history/` - Prediction history

### Alerts & Notifications
- `GET /api/patients/{id}/alerts/` - Patient alerts
- `PUT /api/alerts/{id}/acknowledge/` - Acknowledge alert
- `GET /api/notifications/` - User notifications

## 🗄️ Database Schema

### Core Models
- **Patient**: Demographics, contact info, medical history
- **KidneyMetrics**: eGFR, creatinine, stage, progression data
- **LabResult**: Test results with categorization
- **MLPrediction**: AI predictions with confidence scores
- **Alert**: Critical value notifications
- **Medication**: Active prescriptions and dosages

## 🔬 ML Model Details

### Training Data
- **Dataset**: 1,659 patient records with 54 features
- **Target**: Binary CKD classification (1,524 positive, 135 negative)
- **Features**: Demographics, lab values, symptoms, lifestyle factors

### Feature Selection
- **PCA Analysis**: Dimensionality reduction for optimal performance
- **Selected Features**: 15 most important features identified
- **Model Persistence**: Saved models with joblib for production use

### Clinical Recommendations
Rule-based recommendations based on:
- **eGFR levels**: Stage-specific clinical guidelines
- **Blood pressure**: Hypertension management
- **Proteinuria**: Protein intake recommendations
- **Creatinine**: Kidney function monitoring

## 🏥 Clinical Value

### Early Detection
- Identify CKD risk before clinical symptoms appear
- High recall (98%) minimizes false negatives
- Confidence scores for clinical decision support

### Personalized Care
- Tailored recommendations based on individual patient data
- Stage-specific treatment protocols
- Progression monitoring and alerts

### Healthcare Efficiency
- Automated risk assessment
- Real-time monitoring capabilities
- Comprehensive patient data management

## 🔧 Development

### Project Structure
```
capstone_project/
├── backend/           # Django settings and configuration
├── patients/          # Patient management app
├── medical_data/      # Medical records and metrics
├── ml_predictions/    # ML service and predictions
├── alerts/           # Notification system
├── users/            # Authentication and user management
├── ML/               # Machine learning models and training
└── requirements.txt  # Python dependencies
```

### Running Tests
```bash
python3 manage.py test
```

### API Documentation
Visit `http://localhost:8000/api/docs/` for interactive API documentation.

## 🚀 Production Deployment

### Using Gunicorn
```bash
gunicorn backend.wsgi:application --bind 0.0.0.0:8000
```

## 📈 Performance Metrics

- **Model Accuracy**: 92.47%
- **API Response Time**: <200ms average
- **Database**: SQLite for development, PostgreSQL ready
- **Scalability**: Modular Django architecture

## 🔒 Security Features

- JWT authentication with refresh tokens
- CORS configuration for frontend integration
- Input validation and sanitization
- Secure password hashing
- API rate limiting ready

