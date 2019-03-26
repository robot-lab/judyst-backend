# judyst-backend

## platforms
Данный проект нацелен на платформы Linux. 
Его развертка проводилась на:
- debian 9 - stretch
- debian 9 - testing
- ...

## dependencies
**python3-venv**

Виртуальное окружение python3, позволяет изолировать окружение проекта и использовать библиотеки описанные в requirements.txt 

Для установки: `apt-get install python3-venv`

**rabbitmq-server**

Сервер очередей для поодержки распределнности системы. На данный момент запуск проводился на версии  3.7.11-1.

Для установки: 
- [Офциальная инструкция](https://www.rabbitmq.com/install-debian.html)
- [Первая инструкция](https://www.saqot.com/working/rabbitmq-queue-bundle/setup-rabbitmq-ubuntu.html)
- [Dnjhfz bycnherwbz](https://tecadmin.net/install-rabbitmq-server-debian/)

**postgresql**

Реаляционная база данных. Запуск производился на версиях: 10.5, 9.6

Для установки: [Инструкция](https://linuxize.com/post/how-to-install-postgresql-on-debian-9/)


**requirements.txt**

В файле requirements.txt описанны все зависимости от других питоновских бтблиотек, таких как:
- celery
- django

Для установки: `pip install -r requirements.txt`

## pre run
В этом разделе описываются действия необходимые для успешного запуска проекта.

**Установка переменных среды:**

    $ export USER_NAME=postgres
    $ export BASE_NAME=judyst_backend
    $ export BASE_HOST=127.0.0.1
    $ export BASE_PORT=5432
    $ export BROKER_URL=amqp://guest:guest@localhost:5672/
    $ export BASE_URL=http://127.0.0.1:8000
    $ export BASE_PASSWORD=[secure]

**Запуск внешнекй инфраструктуры:**

    sudo systemctl postgresql start
    sudo systemctl rabbitmq-server start

**Генерация настроек:**

_Стоит отметить, что настройки генерируются из переменных среды._

    python gen_settings.py

**Настройка базы данных:**

_Настройка производится на основе встроенных средств django._

    manage.py makemigrations
    manage.py migrate
    manage.py createsuperuser

## run
После **pre run** можно инициализировать запуск проекта
- `celery worker -A judyst_backend -B ` - для запуска celery, платформы выполнения задач
- `python manage.py runserver ` для запуска сервера, основной точки фхода в систему.
