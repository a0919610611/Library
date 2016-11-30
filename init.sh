#!/bin/sh
rm -rf api/migrations
rm -f db.sqlite3
./manage.py makemigrations api
./manage.py migrate
./manage.py createsuperuser
./manage.py runserver 
