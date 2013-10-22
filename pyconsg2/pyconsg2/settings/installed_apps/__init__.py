"""Installed apps for the pyconsg2 project."""
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
]

EXTERNAL_APPS = [
    'admin_honeypot',
    'debug_toolbar',
    'django_libs',
    'honeypot_signals',
    'mailer',
    'south',
    'rapid_prototyping',
]

INTERNAL_APPS = [
    'pyconsg2',
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + INTERNAL_APPS

from .rapid_prototyping import *  # NOQA
from .debug_toolbar import *  # NOQA
