import os
from pathlib import Path
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = 'independent-mock-local-only'
DEBUG = True
ALLOWED_HOSTS = ['*']
INSTALLED_APPS = ['django.contrib.auth','django.contrib.contenttypes','rest_framework','rest_framework.authtoken','mockapp']
MIDDLEWARE = []
ROOT_URLCONF = 'mockapp.urls'
DATABASES = {'default':{'ENGINE':'django.db.backends.postgresql','NAME':'mock','USER':'envpilot','PASSWORD':'envpilot','HOST':os.getenv('DB_HOST','db')}}
if os.getenv('LAB_SQLITE') == '1':
    DATABASES = {'default':{'ENGINE':'django.db.backends.sqlite3','NAME':BASE_DIR/'local.sqlite3'}}
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
USE_TZ = True
REST_FRAMEWORK = {'DEFAULT_AUTHENTICATION_CLASSES':['rest_framework.authentication.TokenAuthentication'],'DEFAULT_PERMISSION_CLASSES':['rest_framework.permissions.IsAuthenticated'],'TEST_REQUEST_DEFAULT_FORMAT':'json'}
