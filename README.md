# PyCon Singapore 2014 Website

This repository holds the Django 1.6 project that powers the
[https://pycon.sg](https://pycon.sg) website.

## Local Development Environment

You should use OSX or Linux (i.e. Ubuntu).

First, download and install 

* [Virtualbox](https://www.virtualbox.org/wiki/Downloads)
* [Vagrant](https://www.vagrantup.com/downloads.html)

Now install Ansible:

    #!sh
    sudo easy_install-2.7 pip==1.3
    sudo pip install ansible

Clone this repository:

    #!sh
    mkdir -p ~/projects/pyconsg2
    cd ~/projects/pyconsg2
    git clone git@github.com:pythonsingapore/pyconsg2.git src 

Provision the Vagrant box (this will take about 30-60 minutes)

    #!sh
    cd ~/projects/pyconsg2/src
    vagrant up

If `vagrant up` fails it might be that there was a connection issue when
installing packages via `apt-get install`. You can just try to re-run the
provisioning via `vagrant provision`.

Create your `local_settings.py`:

    #!sh
    cd ~/projects/pyconsg2/src/pyconsg2/pyconsg2/settings
    cp local_settings.py.sample local_settings.py
    # Edit the file:
    # - Add your name and email to ADMINS (should be a gmail address)
    # - Enter your Gmail password at EMAIL_HOST_PASSWORD (don't worry, this
    #   file is in .gitignore)

Initialise the database:

    #!sh
    cd ~/projects/pyconsg2/
    vagrant up
    vagrant ssh
    workon pyconsg2 
    cd project/pyconsg2
    ./manage.py syncdb --all --noinput
    ./manage.py migrate --fake
    fab loaddata

Start the development server:

    #!sh
    # inside your vagrant box
    cd ~/project/pyconsg2/
    workon pyconsg2
    fab runserver
    # Visit http://192.168.111.222:8000 in your browser
