#!/bin/bash
sudo /etc/init.d/postgresql start
sudo /etc/init.d/rabbitmq-server start
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python runserver