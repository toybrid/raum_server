#!/usr/bin/env bash
python manage.py migrate
gunicorn raum.wsgi --bind 0.0.0.0:8000 --workers 12