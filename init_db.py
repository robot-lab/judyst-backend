import subprocess
import os
import json


names_for_check = ['python3.6', 'python3', 'python']


def get_python_name():
    """
    Function for getting name of python in system.

    :return:
        Name of python installed in system
    """
    for name in names_for_check:
        try:
            subprocess.run([name, '-c', 'exit()'])
            return name
        except FileNotFoundError:
            pass
    raise FileNotFoundError


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judyst_backend.settings')
    import django
    django.setup()

    executor = get_python_name()
    print(executor, 'used for generation')
    subprocess.run([executor, 'manage.py', 'makemigrations'])
    subprocess.run([executor, 'manage.py', 'migrate'])

    from core.models import DocumentSupertype, AnalyzerType, Analyzer, \
        PropertyType, DataSource, Organisation

    with open('init_db_conf.json') as f_in:
        conf = json.load(f_in)

    for name in conf['DocumentSupertype']:
        DocumentSupertype.objects.create(name=name)
        print('created', 'DocumentSupertype', name)
    for name in conf['AnalyzerType']:
        AnalyzerType.objects.create(name=name)
        print('created', 'AnalyzerType', name)
    for name in conf['PropertyType']:
        PropertyType.objects.create(name=name)
        print('created', 'PropertyType', name)
    Organisation.create(name=conf['Organisation'], is_activated=True)
    print('created', 'Organisation', conf['Organisation'])
    for elem in conf['DataSource']:
        DataSource.objects.create(crawler_name=elem['name'],
                                  source_link=elem['link'])
        print('created', 'DataSource', elem)
    for elem in conf['Analyzer']:
        t = AnalyzerType.objects.get(name=elem['type'])
        Analyzer.objects.create(name=elem['name'], version=elem['version'],
                                analyzer_type=t)
        print('created', 'Analyzer', elem)
