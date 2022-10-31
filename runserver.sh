#!/bin/sh

python manage.py migrate
gunicorn chatbot.wsgi --bind=0.0.0.0:80