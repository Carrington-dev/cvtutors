# from celery import Celery

# app = Celery('flexyweb',
#              broker='amqp://',
#              backend='rpc://',
#              include=['flexyweb.tasks'])

# # Optional configuration, see the application user guide.
# app.conf.update(
#     result_expires=3600,
# )

# if __name__ == '__main__':
#     app.start()
import os
from celery import Celery
# set the default Django settings module for the 'celery' program.


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'flexyweb.settings')

app = Celery('flexyweb')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

