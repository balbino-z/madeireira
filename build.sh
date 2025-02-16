#!/bin/bash
# Comandos para rodar durante o deploy
python manage.py migrate
python manage.py collectstatic --noinput