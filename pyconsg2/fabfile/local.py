from fabric.api import hide, lcd, local

from development_fabfile.fabfile import drop_db, create_db
from development_fabfile.fabfile import rebuild as rebuild_orig


def dumpdata():
    """
    Dumps everything.

    Remember to add new dumpdata commands for new apps here so that you always
    get a full initial dump when running this task.

    """
    local('python2.7 ./manage.py dumpdata --indent 4 --natural auth.user > pyconsg2/fixtures/bootstrap_auth.json')  # NOPEP8
    # account fixtures get created via signals when auth fixtures are loaded
    local('python2.7 ./manage.py dumpdata --indent 4 --natural sites > pyconsg2/fixtures/bootstrap_sites.json')  # NOPEP8

    # django-cms
    local('python2.7 ./manage.py dumpdata --indent 4 --natural cms > pyconsg2/fixtures/bootstrap_cms.json')  # NOPEP8
    local('python2.7 ./manage.py dumpdata --indent 4 --natural djangocms_text_ckeditor > pyconsg2/fixtures/bootstrap_djangocms_text_ckeditor.json')  # NOPEP8

    #local('python2.7 ./manage.py dumpdata --indent 4 --natural conference > pyconsg/fixtures/bootstrap_conference.json')  # NOPEP8
    #local('python2.7 ./manage.py dumpdata --indent 4 --natural speakers > pyconsg/fixtures/bootstrap_speakers.json')  # NOPEP8
    #local('python2.7 ./manage.py dumpdata --indent 4 --natural proposals > pyconsg/fixtures/bootstrap_proposals.json')  # NOPEP8
    #local('python2.7 ./manage.py dumpdata --indent 4 --natural proposals_pyconsg > proposals_pyconsg/fixtures/bootstrap_proposals_pyconsg.json')  # NOPEP8


def loaddata():
    """Loads available fixtures."""
    local('python2.7 manage.py loaddata pyconsg2/fixtures/bootstrap_auth.json')
    local('python2.7 manage.py loaddata pyconsg2/fixtures/bootstrap_sites.json')
    local('python2.7 manage.py loaddata pyconsg2/fixtures/bootstrap_cms.json')
    local('python2.7 manage.py loaddata pyconsg2/fixtures/bootstrap_djangocms_text_ckeditor.json')

    #local('python2.7 manage.py loaddata bootstrap_conference.json')
    #local('python2.7 manage.py loaddata bootstrap_speakers.json')
    #local('python2.7 manage.py loaddata bootstrap_proposals.json')
    #local('python2.7 manage.py loaddata bootstrap_proposals_pyconsg.json')


def rebuild():
    """
    Deletes and re-creates your DB. Needs django-extensions and South.

    """
    drop_db()
    create_db()
    local('python2.7 manage.py syncdb --all --noinput')
    local('python2.7 manage.py migrate --fake')
    loaddata()
