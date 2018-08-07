from webapp import app as webapp
from celery import Celery


def make_celery(app):
    celery = Celery(
        webapp.import_name,
        broker=app.config['CELERY_BROKER_URL'],
        backend=app.config['CELERY_BACKEND']
    )

    celery.conf.update(app.config)
    Taskbase = celery.Task

    class ContextTask(Taskbase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return Taskbase.__call__(self, *args, **kwargs)

    celery.Task = ContextTask

    return celery

celery = make_celery(webapp)


@celery.task()
def log(msg):
    return msg


class MyError(Exception):
    msg = 'My error'


@celery.task()
def add(a, b):
    return a + b


@celery.task(bind=True)
def apptask(self):
    raise MyError()

# celery -A webapp.tasks worker --loglevel=info
