#!/bin/bash
# Comandos para rodar durante o deploy
python manage.py migrate
python manage.py collectstatic --noinput
pip install -r requirements.txt
mkdir -p staticfiles