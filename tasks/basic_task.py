from celery.signals import worker_ready
from django.conf import settings
import celery
from judyst_backend.celery import app


def task_prerun(fn, prerun):
    def wrapped(*args, **kwargs):
        prerun(*args, **kwargs)
        return fn(*args, **kwargs)

    return wrapped


class MetaBaseTask(type):
    def __init__(cls, name, bases, attrs):
        cls.name = name
        cls.run = task_prerun(cls.run, getattr(cls, 'on_prerun'))
        super().__init__(cls)


class BaseTask(celery.Task, metaclass=MetaBaseTask):
    serializer = settings.CELERY_TASK_SERIALIZER
    max_retries = 3
    ignore_result = True
    default_retry_delay = 5

    def __init__(self):
        pass

    def on_prerun(self, *args, **kwargs):
        pass

    def run(self, *args, **kwargs):
        return super().run(*args, **kwargs)

    def on_success(self, retval, task_id, args, kwargs):
        pass


app.tasks.register(BaseTask())


@worker_ready.connect()
def at_start(sender, **k):
    # function that runs when node start
    pass
