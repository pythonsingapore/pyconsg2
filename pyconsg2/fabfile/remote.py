from django.conf import settings

from fabric.api import cd

from development_fabfile.fabfile.utils import require_server, run_workon


@require_server
def run_update_presentations():
    """
    Runs `./manage.py update_presentations` on the given server.

    Usage::

        fab <server> run_update_presentations

    """
    with cd(settings.FAB_SETTING('SERVER_PROJECT_ROOT')):
        run_workon('python2.7 manage.py update_presentations --noinput')
