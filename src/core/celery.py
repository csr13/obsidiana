import os

from celery import Celery


settings = os.getenv("DJANGO_SETTINGS_MODULE", "core.settings.base")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

app = Celery('core')

app.config_from_object("django.conf:settings", namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
