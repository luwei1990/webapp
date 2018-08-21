from celery.schedules import crontab
from webapp import app as webapp

CELERY_IMPORTS = ('webapp.tasks')
CELERY_TASK_RESULT_EXPIRES = 30
CELERY_TIMEZONE = 'UTC'

CELERY_ACCEPT_CONTENT = ['json', 'msgpack', 'yaml']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERYBEAT_SCHEDULE = {
    'test-celery': {
        'task': 'webapp.tasks.print_hello',
        # Every minute
        'schedule': crontab(minute="*"),
    }
}

