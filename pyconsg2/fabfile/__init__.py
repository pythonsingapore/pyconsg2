# flake8: noqa
import os

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE", "pyconsg2.settings")

from development_fabfile.fabfile import *
from .local import *
