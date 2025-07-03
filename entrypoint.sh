#!/bin/sh

set -e

# Run migrations
echo "Running Django migrations..."
python manage.py migrate --noinput

# Collect static files (uncomment for production)
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start Gunicorn
echo "Starting Gunicorn..."
gunicorn myproject.wsgi:application --bind 0.0.0.0:8000 