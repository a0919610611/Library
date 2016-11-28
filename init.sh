#!/bin/sh
rm -rf api/migrations
rm -rf account/migrations
rm -f db.sqlite3
./manage.py makemigrations api
./manage.py makemigrations account
./manage.py migrate
./manage.py createsuperuser
