# judyst-backend

## dependencies
- apt-get install python3-venv
- apt-get install rabbitmq-server
- apt-get install postgresql
- pip install -r requirements.txt

## pre run
- postgresql start
- rabbitmq-server start
- manage.py makemigrations
- manage.py migrate
- manage.py createsuperuser

## run
- `celery worker -A judyst_backend -B ` для запуска celery
- `python manage.py runserver ` для запуска сервера
