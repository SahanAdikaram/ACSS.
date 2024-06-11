#!/bin/sh

# entrypoint.sh

# Run migrations
python manage.py makemigrations
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
# Start the server
exec "$@"
