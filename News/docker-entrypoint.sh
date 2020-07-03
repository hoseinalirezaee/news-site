#!/bin/bash

#blocks until database is available on specified port
while true; do
    TEMP=$(nc -vzw1 "$DATABASE_HOST" "$DATABASE_PORT" 2>&1)
    if [[ "$TEMP" == *"open"* ]]; then
        break
    fi
    sleep 1
done

python manage.py collectstatic --no-input
python manage.py migrate --no-input --skip-checks
python manage.py createsuperuser --username $DJANGO_SUPERUSER_USERNAME --email no@no.com --no-input
python manage.py initdatabase

gunicorn News.wsgi --bind 0.0.0.0:8000 --workers 2 --threads 2
