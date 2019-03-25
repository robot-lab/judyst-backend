
import os




with open("./judyst_backend/local_settings.py", 'w') as f:
    f.write(f"""
DEBUG = True
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '{"BASE_NAME"}',
        'USER': '{"USER_NAME"}',
        'PASSWORD': '{("BASE_PASSWORD")}',
        'HOST': '{("BASE_HOST")}',
        'PORT': '{("BASE_PORT")}',
    }}
}}
BROKER_URL = "{("BROKER_URL")}"
BASE_URL = "{("BASE_URL")}"
ALLOWED_HOSTS = ['*']
""")