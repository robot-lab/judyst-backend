import subprocess
import os
import json
import argparse
import sys
import trafaret as t
from enum import IntEnum


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
    m, created = model.objects.get_or_create(**params)
    if show:
        if created:
            print(f'created {m}')
        else:
            print(f'exist {m}')


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


def create_organisation(name: str, show=False) -> None:
    """
    Function for checking if organisation with given name exist and if not
    create it.

    :param name: str
        Name of organisation.

    :param show: bool
        Flag to show verbose information.
    """
    created = False
    try:
        model = Organisation.objects.get(name=name)
    except ObjectDoesNotExist:
        model = Organisation.create(name=name, is_activated=True)
        created = True
    if show:
        if created:
            print(f'created {model}')
        else:
            print(f'exist {model}')


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


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judyst_backend.settings')
    import django
    django.setup()

    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--python_name', default='python3.6', type=str)
    parser.add_argument('-f', '--file', default='init_db_conf.json', type=str)
    parser.add_argument('-v', '--verbose', action='store_true')
    namespace = parser.parse_args(sys.argv[1:])
    executor = namespace.python_name
    file_name = namespace.file
    verbose = namespace.verbose

    subprocess.run([executor, 'manage.py', 'makemigrations'])
    subprocess.run([executor, 'manage.py', 'migrate'])

    from core.models import DocumentSupertype, AnalyzerType, Analyzer, \
        PropertyType, DataSource, Organisation
    from django.core.exceptions import ObjectDoesNotExist

    try:
        with open(file_name) as f_in:
            conf = json.load(f_in)
    except FileNotFoundError:
        print(f"file {file_name} not found")
        exit(ErrorCodes.NO_SUCH_FILE)
    except json.decoder.JSONDecodeError:
        print(f'file {file_name} is not correct json')
        exit(ErrorCodes.NOT_A_JSON_FILE)

    checker = t.Dict({
        t.Key('DocumentSupertype'): t.List(t.String),
        t.Key('AnalyzerType'): t.List(t.String),
        t.Key('PropertyType'): t.List(t.String),
        t.Key('Organisation', optional=True): t.String,
        t.Key('DataSource'): t.List(t.Dict({
            t.Key('crawler_name'): t.String,
            t.Key('source_link'): t.URL
        })),
        t.Key('Analyzer'): t.List(t.Dict({
            t.Key('name'): t.String,
            t.Key('version'): t.Int,
            t.Key('analyzer_type'): t.String
        }))
    })

    try:
        conf = checker.check(conf)
    except t.DataError:
        print(t.extract_error(checker, conf))
        exit(ErrorCodes.NOT_CORRECT_JSON_STRUCTURE)

    generate_object_by_name(DocumentSupertype, conf['DocumentSupertype'],
                            show=verbose)
    generate_object_by_name(AnalyzerType, conf['AnalyzerType'], show=verbose)
    generate_object_by_name(PropertyType, conf['PropertyType'], show=verbose)

    if 'Organisation' in conf:
        create_organisation(conf['Organisation'], show=verbose)

    for elem in conf['DataSource']:
        loud_model_creation(DataSource, elem, show=verbose)
    for elem in conf['Analyzer']:
        create_analyzer(elem, show=verbose)
