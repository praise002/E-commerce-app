import os     
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myshop.settings')

app = Celery('myshop')
app.config_from_object('django.conf:settings', namespace='CELERY')  # It specifies the prefix
app.autodiscover_tasks()  # Celery to auto-discover asynchronous tasks for your applications.