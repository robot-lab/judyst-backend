import subprocess
import os
import json
import argparse
import sys
import trafaret
import getpass
from enum import IntEnum
from gen_settings import good_view


class ErrorCodes(IntEnum):
    NO_SUCH_FILE = -1
    NOT_A_JSON_FILE = -2
    NOT_CORRECT_JSON_STRUCTURE = -3


def loud_model_creation(model, params: dict, show=False) -> None:
    """
    Function for creating object.

    :param model: Django.model
        Model for creation.

    :param params: dict
        Dictionary with params for model.

    :param show: bool
        Flag to show verbose information.
    """
    instance, created = model.objects.get_or_create(**params)
    if show:
        if created:
            print(f'created {instance}')
        else:
            print(f'exist {instance}')


def generate_object_by_name(model, l: list, show=False) -> None:
    """
    Function for creating many objects from list

    :param model: Django.model
        Model for creation.

    :param l: list
        List with names for creation.

    :param show: bool
        Flag to show verbose information.
    """
    for element in l:
        loud_model_creation(model, {'name': element}, show=show)


def create_analyzer(params: dict, show=False) -> None:
    """
    Function for checking if analyzer with given params exist and if not
    create it.

    :param params: dict
        Name of organisation.

    :param show: bool
        Flag to show verbose information.
    """
    model_params = params.copy()

    try:
        model_params['analyzer_type'] = AnalyzerType.objects.get(
            name=params['analyzer_type'])
    except ObjectDoesNotExist:
        print(f"error analyzer type: {params['analyzer_type']} not presented"
              f" in data base")
        return
    loud_model_creation(Analyzer, model_params, show=show)


def get_var(key: str, allow_input, is_password=False,
            output_sentence='') -> str:
    """
    Function for getting variable value from environment.

    :param key: str
        variable name.

    :param allow_input: bool
        Flag if this param may be inputted from keyboard.

    :param is_password: bool
        Flag if should be used password input or usual.

    :param output_sentence: str
        Sentence for outputting described what user should input.

    :return: str
        variable value.
    """
    result = os.environ.get(key)
    if result is None:
        print(f'In your environment no {key} find.')
        if allow_input:
            if not output_sentence:
                output_sentence = f'Please enter {good_view(key)}: '
            if not is_password:
                return input(output_sentence)
            else:
                return getpass.getpass(output_sentence)
    else:
        return result


def create_superuser(input_fields=False) -> None:
    """
    Function for checking if such user exist and if exist switch this user to
    super user.

    :param input_fields: bool
        Flag if an found fields should be inputted from keyboard or stop
        creation.
    """
    username = get_var('SUPERUSER_USERNAME', input_fields)
    if not username:
        print('incorrect username')
        return
    email = get_var('SUPERUSER_EMAIL', input_fields)
    if not email:
        print('incorrect email')
        return
    password = get_var('SUPERUSER_PASSWORD', input_fields, is_password=True)
    second_password = get_var('SUPERUSER_PASSWORD', input_fields,
                              is_password=True,
                              output_sentence='Please enter superuser '
                                              'password again: ')
    if not password:
        print('incorrect password')
        return
    if not second_password:
        print('incorrect second_password')
        return
    if password != second_password:
        print('password mismatch')
        return

    try:
        user = CustomUser.objects.get(username=username)
        if not user.is_staff:
            print(f'user {username} exists and it is not staff')
            return
        if not user.is_superuser:
            print(f'user {username} exists but not a superuser')
            return
        print(f'superuser {username} already exists')
    except CustomUser.DoesNotExist:
        CustomUser.objects.create_superuser(username, email, password)
        print(f'superuser {username} created')


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judyst_backend.settings')
    import django
    django.setup()

    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--python_name', default='python3.6', type=str,
                        help='python name for execute django preparation '
                             'scripts')
    parser.add_argument('-f', '--file', default='init_db_conf.json', type=str,
                        help='file with data for inserting to database')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='flag for showing information about data '
                             'inserting')
    parser.add_argument('-su', '--super_user', action='store_true',
                        help='flag if superuser should be created')
    parser.add_argument('-i', '--input', action='store_true',
                        help='flag if superuser fields may be inputted from '
                             'keyboard')
    namespace = parser.parse_args(sys.argv[1:])
    executor = namespace.python_name
    file_name = namespace.file
    verbose = namespace.verbose

    subprocess.run([executor, 'manage.py', 'makemigrations'])
    subprocess.run([executor, 'manage.py', 'migrate'])

    from core.models import DocumentSupertype, AnalyzerType, Analyzer, \
        PropertyType, DataSource, Organisation, CustomUser
    from django.core.exceptions import ObjectDoesNotExist

    if namespace.super_user:
        create_superuser(namespace.input)

    try:
        with open(file_name) as f_in:
            conf = json.load(f_in)
    except FileNotFoundError:
        print(f"file {file_name} not found")
        exit(ErrorCodes.NO_SUCH_FILE)
    except json.decoder.JSONDecodeError:
        print(f'file {file_name} is not correct json')
        exit(ErrorCodes.NOT_A_JSON_FILE)

    checker = trafaret.Dict({
        trafaret.Key('DocumentSupertype'): trafaret.List(trafaret.String),
        trafaret.Key('AnalyzerType'): trafaret.List(trafaret.String),
        trafaret.Key('PropertyType'): trafaret.List(trafaret.String),
        trafaret.Key('Organisation', optional=True): trafaret.String,
        trafaret.Key('DataSource'): trafaret.List(trafaret.Dict({
            trafaret.Key('crawler_name'): trafaret.String,
            trafaret.Key('source_link'): trafaret.URL
        })),
        trafaret.Key('Analyzer'): trafaret.List(trafaret.Dict({
            trafaret.Key('name'): trafaret.String,
            trafaret.Key('version'): trafaret.Int,
            trafaret.Key('analyzer_type'): trafaret.String
        }))
    })

    try:
        conf = checker.check(conf)
    except trafaret.DataError:
        print(trafaret.extract_error(checker, conf))
        exit(ErrorCodes.NOT_CORRECT_JSON_STRUCTURE)

    generate_object_by_name(DocumentSupertype, conf['DocumentSupertype'],
                            show=verbose)
    generate_object_by_name(AnalyzerType, conf['AnalyzerType'], show=verbose)
    generate_object_by_name(PropertyType, conf['PropertyType'], show=verbose)

    if 'Organisation' in conf:
        loud_model_creation(Organisation, {'name': conf['Organisation'],
                                           'is_activated': True}, show=verbose)

    for elem in conf['DataSource']:
        loud_model_creation(DataSource, elem, show=verbose)
    for elem in conf['Analyzer']:
        create_analyzer(elem, show=verbose)
