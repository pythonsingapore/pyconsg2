"""URLs for the pyconsg2 project."""
from django.conf import settings
from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import RedirectView, TemplateView

from django_libs.views import RapidPrototypingView

from pyconsg2.views import AdminStacksView


admin.autodiscover()


class TextPlainView(TemplateView):
  def render_to_response(self, context, **kwargs):
    return super(TextPlainView, self).render_to_response(
      context, content_type='text/plain', **kwargs)


urlpatterns = patterns('',
    url(r'^jsi18n/(?P<packages>\S+?)/$',
        'django.views.i18n.javascript_catalog'
    ),
    url(r'^robots\.txt', TextPlainView.as_view(template_name='robots.txt')),
    url(r'^favicon\.ico', RedirectView.as_view(url='/static/favicon.ico')),
)

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()

if settings.DEBUG is False and settings.SANDBOX is True:
    # If you want to set DEBUG=False on your local machine, Django would no
    # longer serve static files and you would have to setup Apache or Nginx.
    # This hack allows Django to serve staticfiles (which is slow and insecure)
    urlpatterns += patterns(
        '',
        (r'^404/$', 'django.views.defaults.page_not_found'),
        (r'^500/$', 'django.views.defaults.server_error'),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.STATIC_ROOT}),
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve',
            {'document_root': settings.MEDIA_ROOT}),
    )


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += patterns(
        '',
        url(r'^__debug__/', include(debug_toolbar.urls)),
    )


urlpatterns += patterns(
    '',
    url(r'^admin-stacks/', AdminStacksView.as_view(), name='admin_stacks'),
    url(settings.ADMIN_URL, include(admin.site.urls)),

    url(r'^checkout/group/', include('paypal_pyconsg.group_checkout_urls')),
    # url(r'^checkout/',
    #    TemplateView.as_view(template_name='checkout_closed.html'),
    #    name='paypal_checkout'),
    url(r'^checkout/', include('paypal_express_checkout.urls')),
    url(r'^paypal/', include('paypal_pyconsg.admin_urls')),
    url(r'^dashboard/checkout-choices/', include('paypal_pyconsg.urls')),
    url(r'^impersonate/', include('impersonate.urls')),
    url(r'^group-registrations/', include('group_registrations.urls')),

    url(r'^', include('pyconsg2.symposion_urls')),
    url(r'^', include('cms.urls')),
)
