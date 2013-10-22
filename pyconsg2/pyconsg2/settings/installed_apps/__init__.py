"""Installed apps for the pyconsg2 project."""
DJANGO_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djangocms_admin_style',
    'django.contrib.admin',
]

EXTERNAL_APPS = [
    # normal apps, sorted alphabetically
    'admin_honeypot',
    'debug_toolbar',
    'django_libs',
    'honeypot_signals',
    'mailer',
    'south',

    # django-cms apps
    'djangocms_text_ckeditor',  # must come before cms
    'cms',
    'cms.stacks',
    'filer',
    'mptt',
    'menus',
    'sekizai',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
]

INTERNAL_APPS = [
    'pyconsg2',
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + INTERNAL_APPS

from .cms import *  # NOQA
from .debug_toolbar import *  # NOQA
from .djangocms_text_ckeditor import *  # NOQA
