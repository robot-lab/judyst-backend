import os


def good_view(variable_name):
    return variable_name.lower().replace('_', ' ')


def get_var(key: str) -> str:
    result = os.environ.get(key)
    if result is None:
        print(f'In your environment no {key} find.')
        return input(f'Please enter {good_view(key)}: ')
    else:
        return result


with open("./judyst_backend/local_settings.py", 'w') as f:
    f.write(f"""
# debug flag
DEBUG = True

# database settings
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{get_var("BASE_NAME")}',
        'USER': '{get_var("USER_NAME")}',
        'PASSWORD': '{get_var("BASE_PASSWORD")}',
        'HOST': '{get_var("BASE_HOST")}',
        'PORT': '{get_var("BASE_PORT")}',
    }}
}}

# celery broker url, for ex: "amqp://guest:guest@localhost:5672/"
BROKER_URL = "{get_var("BROKER_URL")}"

# site settings
BASE_URL = "{get_var("BASE_URL")}"
ALLOWED_HOSTS = ['*']

# security information
SECRET_KEY = "{get_var("SECRET_KEY")}"
""")
