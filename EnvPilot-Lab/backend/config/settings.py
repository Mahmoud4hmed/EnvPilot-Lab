import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'envpilot-local-fictional-data-only'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['django.contrib.auth', 'django.contrib.contenttypes', 'rest_framework', 'rest_framework.authtoken', 'lab']
MIDDLEWARE = ['django.middleware.security.SecurityMiddleware', 'django.middleware.common.CommonMiddleware']
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql', 'NAME': os.getenv('POSTGRES_DB', 'envpilot'), 'USER': 'envpilot', 'PASSWORD': 'envpilot', 'HOST': os.getenv('DB_HOST', 'db'), 'PORT': os.getenv('DB_PORT', '5432')}}
# A convenience for local syntax/unit validation only; concurrency grading requires PostgreSQL.
if os.getenv('LAB_SQLITE') == '1':
    DATABASES = {'default': {'ENGINE': 'django.db.backends.sqlite3', 'NAME': BASE_DIR / 'local.sqlite3'}}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True
TIME_ZONE = 'UTC'
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES': ['rest_framework.authentication.TokenAuthentication'], 'DEFAULT_PERMISSION_CLASSES': ['rest_framework.permissions.IsAuthenticated'], 'EXCEPTION_HANDLER': 'lab.errors.exception_handler', 'TEST_REQUEST_DEFAULT_FORMAT': 'json'}
CELERY_BROKER_URL = os.getenv('BROKER_URL', 'redis://redis:6379/0')
CELERY_RESULT_BACKEND = CELERY_BROKER_URL
CELERY_TASK_DEFAULT_QUEUE = 'provision'
CELERY_TASK_ALWAYS_EAGER = False
CELERY_TASK_TRACK_STARTED = True
CELERY_TASK_SOFT_TIME_LIMIT = 10
CELERY_TASK_TIME_LIMIT = 15
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 30}
PROVIDER_URL = os.getenv('PROVIDER_URL', 'http://provider:9000')
