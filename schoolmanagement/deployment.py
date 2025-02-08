import os
from .settings import *
from .settings import BASE_DIR
import dj_database_url

SECRET_KEY = os.getenv('SECRET_KEY')
ALLOWED_HOSTS = os.getenv('DJANGO_ALLOWED_HOSTS', '127.0.0.1,localhost,kutlwanong-3xhqp.ondigitalocean.app').split(',')
CSRF_TRUSTED_ORIGINS = ['https://' + domain for domain in ALLOWED_HOSTS]
DEBUG = False

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

connection_string = os.environ['DATABASE_CONNECTIONS']
parameters = {pair.split('=')[0]: pair.split('=')[1] for pair in connection_string.split(' ')}
# connection_string = os.environ['AZURE_POSTGRESQL_CONNECTIONS']
#parameters = {pair.split('='):pair.split('=')[1] for pair in connection_string.split(' ')}


DATABASE_URL = os.getenv("DATABASE_URL")

if DATABASE_URL:
    DATABASES = {
        'default': dj_database_url.config(default=DATABASE_URL)
    }
else:
    print("Warning: DATABASE_URL is not set. Using SQLite as fallback.")
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
        }
    }

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': parameters['dbname'],
#         'HOST': parameters['host'],
#         'USER': parameters['user'],
#         'PASSWORD': parameters['password'],
#     }
# }
