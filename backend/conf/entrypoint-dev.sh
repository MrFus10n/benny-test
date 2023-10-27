#!/bin/bash

# If command is entered, run command. Else, start dev server.
# Command example: docker-compose run --rm backend python manage.py createsuperuser
if [ "$#" != "0" ]; then
    exec "$@"
else
    python manage.py migrate  # This is for test task only
    exec python manage.py runserver 0.0.0.0:8000
fi
