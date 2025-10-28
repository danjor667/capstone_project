#!/bin/bash

# CKD Digital Twin Build Script

echo "🏗️  Building CKD Digital Twin Project..."

# Install dependencies
echo "📦 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python3 manage.py makemigrations
python3 manage.py migrate

# Create superuser
echo "👤 Creating admin user..."
python3 manage.py shell -c "
from django.contrib.auth.models import User
if not User.objects.filter(email='admin@gmail.com').exists():
    User.objects.create_superuser('admin', 'admin@gmail.com', '1234')
    print('✅ Admin user created: admin@gmail.com / 1234')
else:
    print('ℹ️  Admin user already exists')
"

# Collect static files
echo "📁 Collecting static files..."
python3 manage.py collectstatic --noinput

echo "✅ Build complete! You can now run:"
echo "   python3 manage.py runserver"