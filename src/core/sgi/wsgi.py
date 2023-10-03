import os

from django.core.wsgi import get_wsgi_application


settings = os.getenv("DJANGO_SETTINGS_MODULE", "core.configs.dev")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

application = get_wsgi_application()

