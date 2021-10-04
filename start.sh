#!/bin/sh

echo "Apply database migrations"
python manage.py migrate

echo "Starting server"
gunicorn --bind 0.0.0.0:8585 --workers 1 --log-level INFO card_manager.wsgi:application
