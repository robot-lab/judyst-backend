import subprocess
import os
import json
import argparse
import sys


def loud_model_creation(model, params: dict, show=False) -> None:
    """
    Function for creating object.

    :param model: Django.model
        Model for creation.

    :param params: dict
        Dictionary with params for model.

    :param show: bool
        Flag to show verbose information
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
        Flag to show verbose information
    """
    for element in l:
        loud_model_creation(model, {'name': element}, show=show)


def check_fields(old_dict:dict, fields: list)->(None, dict):
    """
    Function for making copy of dict with needed fields or return None if not
    all fields represented.

    :param old_dict: dict
        Dictionary with presented fields.

    :param fields: list
        Fields for checking

    :return: (None, dict)
        Return dict if all fields presented or None otherwise.
    """
    res = {}
    for field_name in fields:
        if field_name not in old_dict:
            print(f'error no field {field_name} in {old_dict}')
            return
        else:
            res[field_name] = old_dict[field_name]
    return res


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
        exit(-1)
    except json.decoder.JSONDecodeError:
        print(f'file {file_name} is not correct json')
        exit(-2)

    if 'DocumentSupertype' in conf and isinstance(conf['DocumentSupertype'],
                                                  list):
        generate_object_by_name(DocumentSupertype,
                                conf['DocumentSupertype'], show=verbose)
    if 'AnalyzerType' in conf and isinstance(conf['AnalyzerType'], list):
        generate_object_by_name(AnalyzerType,
                                conf['AnalyzerType'], show=verbose)
    if 'PropertyType' in conf and isinstance(conf['PropertyType'], list):
        generate_object_by_name(PropertyType,
                                conf['PropertyType'], show=verbose)
    if 'Organisation' in conf and not \
            Organisation.objects.filter(name=conf['Organisation']).exists():
        loud_model_creation(Organisation, {'name': conf['Organisation'],
                             'is_activated': True}, show=verbose)

    if 'DataSource' in conf and isinstance(conf['DataSource'], list):
        for elem in conf['DataSource']:
            d = check_fields(elem, ['crawler_name', 'source_link'])
            if d:
                loud_model_creation(DataSource, d, show=verbose)
    if 'Analyzer' in conf and isinstance(conf['Analyzer'], list):
        for elem in conf['Analyzer']:
            d = check_fields(elem, ['name', 'version'])

            if 'analyzer_type' not in elem:
                print(f'error no analyzer type in {elem}')
                continue

            try:
                analyzer_type = AnalyzerType.objects.get(
                    name=elem['analyzer_type'])
            except ObjectDoesNotExist:
                print(f"error analyzer type: {elem['analyzer_type']} "
                      f"not presented in data base")
                continue
            d['analyzer_type'] = analyzer_type
            loud_model_creation(Analyzer, d, show=verbose)
