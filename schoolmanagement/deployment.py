import os
from .settings import *
from .settings import BASE_DIR
import dj_database_url

SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')
ALLOWED_HOSTS = os.getenv('WEBSITE_HOSTNAME', 'shark-app-4gdck.ondigitalocean.app').split(',')
CSRF_TRUSTED_ORIGINS = ['https://' + domain for domain in os.getenv('WEBSITE_HOSTNAME', 'shark-app-4gdck.ondigitalocean.app').split(',')]
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


DATABASES = {
    'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
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
