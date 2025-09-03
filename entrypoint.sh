#!/bin/sh
# Ejecuta las migraciones si es necesario
echo "Microservice Landings"
echo "Waiting for PostgreSQL to be ready..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."
echo "Running makemigrations and migrate..."

python manage.py makemigrations landing
python manage.py makemigrations
python manage.py migrate

# Exportar variable para signals
export DJANGO_RUNNING_MIGRATIONS=True

# Recopila archivos estáticos para Swagger
echo "Collecting static files for Swagger..."
python manage.py collectstatic --noinput
python manage.py load_default_data

# Inicia el servidor con gunicorn
echo "Starting the server with gunicorn..."
watchmedo auto-restart --directory=./ --pattern=*.py --recursive -- gunicorn -b 0.0.0.0:8080 app.wsgi:application
