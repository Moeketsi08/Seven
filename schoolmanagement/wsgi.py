"""
WSGI config for schoolmanagement project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

settings_module  = 'schoolmanagement.deployment' if 'WEBSITE_HOSTNAME' in os.environ else 'schoolmanagement.settings'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
