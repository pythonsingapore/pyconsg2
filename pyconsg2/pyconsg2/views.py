"""Special views for the pyconsg project."""
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView


class AdminStacksView(TemplateView):
    """
    View that renders stacks that are otherwise hard to reach.

    For example the signup page cannot be reached by an authenticated user
    and therefore an admin would have no chance to edit the stack on that page.

    """
    template_name = 'pyconsg/admin_stacks.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_staff:
            raise Http404
        return super(AdminStacksView, self).dispatch(
            request, *args, **kwargs)
