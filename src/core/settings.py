import os
from pathlib import Path

from core.dj_extensions import rest_framework, simple_jwt


BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))

BASE_DIR = Path(BASE_DIR)

SECRET_KEY = os.getenv('SECRET_KEY', 'fkjsdhfgjksdgnfsdkjgfds43321423')

DEBUG = os.getenv('DEBUG', True)

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS')
if ALLOWED_HOSTS is None:
    ALLOWED_HOSTS = ["*"]

API_PREFIX = os.getenv('API_PREFIX', 'api')

API_VERSIONS = os.getenv('API_VERSIONS', 'v1')

APPEND_SLASH = False

FIXTURE_DIRS = [BASE_DIR / "fixtures"]

INSTALLED_APPS = [
    'admin_extend',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'django_extensions',
    'rest_framework',
    'corsheaders',
    'rest_framework_simplejwt',
    'drf_yasg',
]

APPLICATION_APPS = [
    'users',
    'proxies',
    'apis.scanners.scan',
    'apis.scanners.dirby',
    'apis.scanners.sslyze',
    'apis.scanners.wafw00f',
    'apis.scanners.scanvus',
]

INSTALLED_APPS += THIRD_PARTY_APPS + APPLICATION_APPS

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'core.middlewares.scanners.AvailableScannersMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "admin_extend" / "templates" / "admin"
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.sgi.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.ScryptPasswordHasher',
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
]

AUTH_USER_MODEL = "users.User"

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

STATIC_ROOT = BASE_DIR / "static"

STATICFILES_DIRS = [
    BASE_DIR / "admin_extend" / "assets"
]

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Settings
CORS_ALLOW_ALL_ORIGINS = False

CORS_ALLOWED_ORIGINS = [
    'http://localhost:3000',
]
# CELERY
CELERY_BROKER_URL = os.getenv("REDIS_URL")

CELERY_RESULT_BACKEND = os.getenv("REDIS_URL")

SCANNERS_AVAILABLE = {
    1 : "dirby",
#    2 : "scanvus",
    3 : "sslyze",
    5 : "wafwoof",
    7 : "wafw00f",
    8 : "whatweb",
    #8 : "cvescannerv2",
}

SCANNERS_AVAILABLE_LIST = [
    scanner for scanner in SCANNERS_AVAILABLE.values()
]

API_ENABLED = False

if API_ENABLED:
    REST_FRAMEWORK = rest_framework.REST_FRAMEWORK_CONFIG.settings()
    SIMPLE_JWT = simple_jwt.SIMPLE_JWT_CONFIG(SECRET_KEY).settings()
    SWAGGER_SETTINGS = {
        'SECURITY_DEFINITIONS': {
            'Bearer': {
                'type': 'apiKey',
                'name': 'Authorization',
                'in': 'header'
            }
        }
    }
