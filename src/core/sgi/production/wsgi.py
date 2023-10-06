from django.core.wsgi import get_wsgi_application


settings = os.getenv("DJANGO_SETTINGS_MODULE", "core.configs.prod")

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings)

application = get_wsgi_application()

