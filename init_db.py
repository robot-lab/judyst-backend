import subprocess
import os
import json
import argparse
import sys


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'judyst_backend.settings')
    import django
    django.setup()

    parser = argparse.ArgumentParser()
    parser.add_argument('-pn', '--python_name', default='python3.6', type=str)
    namespace = parser.parse_args(sys.argv[1:])
    executor = namespace.python_name

    subprocess.run([executor, 'manage.py', 'makemigrations'])
    subprocess.run([executor, 'manage.py', 'migrate'])

    from core.models import DocumentSupertype, AnalyzerType, Analyzer, \
        PropertyType, DataSource, Organisation

    with open('init_db_conf.json') as f_in:
        conf = json.load(f_in)

    for name in conf['DocumentSupertype']:
        DocumentSupertype.objects.get_or_create(name=name)
        print('created', 'DocumentSupertype', name)
    for name in conf['AnalyzerType']:
        AnalyzerType.objects.get_or_create(name=name)
        print('created', 'AnalyzerType', name)
    for name in conf['PropertyType']:
        PropertyType.objects.get_or_create(name=name)
        print('created', 'PropertyType', name)
    if not Organisation.objects.filter(name=conf['Organisation']).exists():
        Organisation.create(name=conf['Organisation'], is_activated=True)
    print('created', 'Organisation', conf['Organisation'])
    for elem in conf['DataSource']:
        DataSource.objects.get_or_create(crawler_name=elem['name'],
                                         source_link=elem['link'])
        print('created', 'DataSource', elem)
    for elem in conf['Analyzer']:
        analyzer_type = AnalyzerType.objects.get(name=elem['type'])
        Analyzer.objects.get_or_create(name=elem['name'],
                                       version=elem['version'],
                                       analyzer_type=analyzer_type)
        print('created', 'Analyzer', elem)
