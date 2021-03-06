# judyst-backend

## platforms
Данный проект нацелен на платформы Linux. 
Его развертка проводилась на:
- debian 9 - stretch
- debian 9 - testing
- ...

## dependencies
**python3-venv**

Виртуальное окружение python3.
Позволяет изолировать окружение проекта и использовать библиотеки описанные в requirements.txt 

Для установки: `apt-get install python3-venv`

**rabbitmq-server**

Сервер очередей для поддержки распределенности системы. На данный момент запуск проводился на версии  3.7.11-1.

Для установки: 
- [Официальная инструкция](https://www.rabbitmq.com/install-debian.html)
- [Первая инструкция](https://www.saqot.com/working/rabbitmq-queue-bundle/setup-rabbitmq-ubuntu.html)
- [Вторвая инструкция](https://tecadmin.net/install-rabbitmq-server-debian/)

**postgresql**

Реляционная база данных. Запуск производился на версиях: 10.5, 9.6

Для установки: [Инструкция](https://linuxize.com/post/how-to-install-postgresql-on-debian-9/)


**requirements.txt**

В файле requirements.txt описаны все зависимости от других питоновских библиотек, таких как:
- celery
- django

Для установки: 
    
    `pip install -r requirements.txt`

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
    $ export SUPERUSER_USERNAME=admin
    $ exprot SUPERUSER_EMAIL=youremail@gmail.com
    $ export SUPERUSER_PASSWORD=[secure]

**Запуск внешней инфраструктуры:**

    sudo systemctl postgresql start
    sudo systemctl rabbitmq-server start

**Генерация настроек:**

_Стоит отметить, что настройки генерируются из переменных среды._

    python gen_settings.py
    
Для генерации случайных значений можно использовать команду: `python gen_settings.py -ag SECRET_KEY -l 34 -i True`

**Настройка базы данных:**

_Настройка производится на основе скрипта `init_db.py` и встроенных средств django._

    python init_db.py

Если в системе не установлен python3.6 или используется другой alias то необзодимо его указать через флаг `-np`, для получении детальной информации о заполении базы данных можно добавить флаг `-v`.
По умолчанию используется файл `init_db_conf.json` для использования другого файла можно сипользовать файл `-f` с указанием пути до файла.  
Если добавить флаг `-cu` то будет создан суперпользователь с параметрами `SUPERUSER_USERNAME`(имя пользователя), `SUPERUSER_EMAIL`(электронная почта), `SUPERUSER_PASSWORD`(пароль пользователя) взятые из системы. Также если добавить флаг `-i` то недостающие параметры можно будет ввестис клавиатуры.  
Коды возвращаемых ошибок: 
1. -1 - не найден указанный файл
2. -2 - файл содержит не корректный json
3. -3 - ошибка содержания полей в json подробнее об ошибке смотри в потоке вывода

Также суперпользователя можно создать вооспользовавшись встроенной командой:

    manage.py createsuperuser

## run
После **pre run** можно инициализировать запуск проекта
- `celery worker -A judyst_backend -B ` - для запуска celery, платформы выполнения задач
- `python manage.py runserver ` для запуска сервера, основной точки входа в систему.
