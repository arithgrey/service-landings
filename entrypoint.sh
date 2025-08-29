#!/bin/sh
# Ejecuta las migraciones si es necesario
echo "Microservice Landings"
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."

python manage.py makemigrations landing
python manage.py makemigrations
python manage.py migrate

# Inicia el servidor con gunicorn
echo "Starting the server with gunicorn..."
gunicorn -b 0.0.0.0:8000 app.wsgi:application --reload
