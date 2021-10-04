#!/bin/sh

echo "Collect static files"
python manage.py collectstatic --noinput

echo "Apply database migrations"
python manage.py makemigrations
python manage.py migrate
echo "from core.models import Person; Person.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell

echo "Starting server"
python manage.py runserver_plus 0.0.0.0:8585
