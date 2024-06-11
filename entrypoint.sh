#!/bin/sh

# entrypoint.sh

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Start the server
exec "$@"
