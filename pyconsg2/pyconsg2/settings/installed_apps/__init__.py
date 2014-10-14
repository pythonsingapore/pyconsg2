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
    'debug_toolbar',
    'django_extensions',
    'django_libs',
    'easy_thumbnails',
    'hvad',
    'mailer',
    # 'simple_translation',
    'south',
    'paypal_express_checkout',
    'paypal_pyconsg',

    # django-cms apps
    'djangocms_text_ckeditor',  # must come before cms
    'cms',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_image',
    'cmsplugin_template_placeholder',
    'filer',
    'menus',
    'mptt',
    'multilingual_news',
    'people',
    'document_library',
    'multilingual_tags',
    'sekizai',

    # external symposion related
    'timezones',
    'metron',
    'markitup',
    'taggit',
    'account',
    'reversion',

    # symposion
    'symposion',
    'symposion.sponsorship',
    'symposion.conference',
    'symposion.boxes',
    'symposion.proposals',
    'symposion.speakers',
    'symposion.teams',
    'symposion.reviews',
    'symposion.schedule',

    'influxdb_metrics',
]

INTERNAL_APPS = [
    'favourite_talks',
    'group_registrations',
    'pyconsg2',
    'proposals_pyconsg',
]

INSTALLED_APPS = DJANGO_APPS + EXTERNAL_APPS + INTERNAL_APPS

from .account import *  # NOQA
from .cms import *  # NOQA
from .debug_toolbar import *  # NOQA
from .djangocms_text_ckeditor import *  # NOQA
from .easy_thumbnails import *  # NOQA
from .impersonate import *  # NOQA
from .markitup import *  # NOQA
from .paypal_express_checkout import *  # NOQA
from .symposion import *  # NOQA
