#!/bin/bash
gunicorn backend.wsgi:application --bind 0.0.0.0:10000
python manage.py runserver --settings=backend.settings 0.0.0.0:80
