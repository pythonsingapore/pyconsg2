# flake8: noqa
"""
URLs needed by the symposion app.

See https://github.com/pinax/pinax-project-symposion/blob/master/project_name/urls.py

"""
from django.conf.urls.defaults import include, patterns, url


import symposion.views


WIKI_SLUG = r'(([\w-]{2,})(/[\w-]{2,})*)'


urlpatterns = patterns('',
    url(r'^account/signup/$', symposion.views.SignupView.as_view(), name='account_signup'),
    url(r'^account/login/$', symposion.views.LoginView.as_view(), name='account_login'),
    url(r'^account/', include('account.urls')),

    url(r'^dashboard/', symposion.views.dashboard, name='dashboard'),
    url(r'^speaker/', include('symposion.speakers.urls')),
    url(r'^proposals/', include('symposion.proposals.urls')),
    url(r'^sponsors/', include('symposion.sponsorship.urls')),
    url(r'^boxes/', include('symposion.boxes.urls')),
    url(r'^teams/', include('symposion.teams.urls')),
    url(r'^reviews/', include('symposion.reviews.urls')),
    url(r'^schedule/', include('symposion.schedule.urls')),
    url(r'^markitup/', include('markitup.urls')),
)
