#!/bin/bash
set -e

echo "Running migrations..."
python manage.py migrate --noinput

echo "Starting gunicorn..."
exec gunicorn --config gunicorn.conf.py ameaozon.wsgi:application
