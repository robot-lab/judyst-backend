import subprocess


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
    executor = get_python_name()
    print(executor, 'used for generation')
    subprocess.run([executor, 'manage.py', 'makemigrations'])
    subprocess.run([executor, 'manage.py', 'migrate'])
