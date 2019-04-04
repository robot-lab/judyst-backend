import sys
import os
import random
import string
import argparse

auto_gen_len = 17
keys_for_auto_gen = []


def good_view(variable_name: str) -> str:
    """
    Function for make pretty names of environmental variables.

    :param variable_name: str
        name of env variable.

    :return: str
        pretty view.
    """
    return variable_name.lower().replace('_', ' ')


def rnd_gen() -> str:
    """
    function for generating random strings
    :return: string
        random string fixed length
    """
    return ''.join(random.choice(string.digits + string.ascii_letters) for _ in range(auto_gen_len))


def get_var(key: str) -> str:
    """
    Function for getting variable value from environment.

    :param key: str
        variable name.

    :return: str
        variable value.
    """
    if key in keys_for_auto_gen:
        return rnd_gen()
    result = os.environ.get(key)
    if result is None:
        print(f'In your environment no {key} find.')
        return input(f'Please enter {good_view(key)}: ')
    else:
        return result


def print_template():
    """
    function for printing template to the local_settings.py file

    :return: None
    """
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


if __name__=="__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ag', '--auto_generation', nargs='+', default=[], type=str)
    parser.add_argument('-l', '--len', default=17, type=int)
    namespace = parser.parse_args(sys.argv[1:])
    auto_gen_len = namespace.len
    keys_for_auto_gen = namespace.auto_generation
    print_template()
