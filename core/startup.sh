#!/bin/sh

python manage.py makemigrations
python manage.py migrate

if python manage.py shell -c "from django.contrib.auth.models import User; exit(0) if User.objects.filter(username='admin').exists() else exit(1)"; then
    echo "Superuser already exists"
else
    echo "Creating superuser..."
    python manage.py createsuperuser --no-input
fi

python manage.py runserver 0.0.0.0:8000
